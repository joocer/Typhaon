"""
Schema Validation
Tests a dictionary against a schema to test for conformity.
Schema definition is similar to - but not the same as - avro schemas
Supported Types:
    - string - a character sequence
        - format
    - numeric - a number
        - min:
        - max
    - date - a datetime.date or an iso format date or time
    - boolean - a boolean or a binary value (true/false, on/off, yes/no)
        - symbols
    - other - not one of the above, but a required field
    - nullable - Python Falsy (None, 0, Empty String, etc)
    - enum - 
        - symbols
Example Schema:
{
 "name": "Table Name",
 "fields": [
     {"name": "id", "type": "string"},
     {"name": "country",  "type": ["string", "nullable"]},
     {"name": "followers", "type": ["string", "nullable"]}
 ]
}
"""
import datetime
from typing import List, Any, Union, Callable
import os
import re
import json


# compatibility
serialize = json.dumps
parse = json.loads


VALID_BOOLEAN_VALUES = ("true", "false", "on", "off", "yes", "no", "0", "1")
DEFAULT_MIN = -9223372036854775808
DEFAULT_MAX = 9223372036854775807


class is_string():
    __slots__ = ['pattern', 'regex']
    def __init__(self, **kwargs):
        self.regex = None
        self.pattern = kwargs.get('format')
        if self.pattern:
            self.regex = re.compile(self.pattern)
    def __call__(self, value: Any) -> bool:
        if self.pattern:
            return self.regex.match(str(value))
        else:
            return type(value).__name__ == "str"
    def __str__(self):
        if self.pattern:
            return f'string {self.pattern}'
        else:
            return 'string'

class is_valid_enum():
    __slots__ = ['symbols']
    def __init__(self, **kwargs):
        """
        -> "type": "enum", "symbols": ["up", "down"]
        
        symbols: list of allowed values (case sensitive)
        """
        self.symbols = kwargs.get('symbols', ())
    def __call__(self, value: Any) -> bool:
        return value and value in self.symbols
    def __str__(self):
        return f'enum {self.symbols}'


class is_boolean(is_valid_enum):
    def __init__(self, **kwargs):
        """
        is_boolean is a special implementation of is_valid_enum
        - it defaults to a set of true/false values
        - the check is case insensitive
        """
        super().__init__()
        self.symbols = VALID_BOOLEAN_VALUES
    def __call__(self, value: Any) -> bool:
        return super().__call__(str(value).lower())


class is_numeric():
    __slots__ = ['min', 'max']
    def __init__(self, **kwargs):
        """
        -> "type": "numeric", "min": 0, "max": 100
        
        min: low end of valid range
        max: high end of valid range
        """
        self.min = kwargs.get('min', DEFAULT_MIN)
        self.max = kwargs.get('max', DEFAULT_MAX)
    def __call__(self, value: Any) -> bool:
        try:
            n = float(value)
        except ValueError:
            return False
        except TypeError:
            return False
        return (n >= self.min) and (n <= self.max)
    def __str__(self):
        if self.min == DEFAULT_MIN and self.max == DEFAULT_MAX:
            return 'numeric'
        if not self.min == DEFAULT_MIN and not self.max == DEFAULT_MAX:
            return f'numeric ({self.min} - {self.max})'
        if not self.min == DEFAULT_MIN and self.max == DEFAULT_MAX:
            return f'numeric ({self.min} - infinity)'
        if self.min == DEFAULT_MIN and not self.max == DEFAULT_MAX:
            return f'numeric (infinity - {self.max})'


def is_date(value: Any) -> bool:
    try:
        if type(value).__name__ in ["datetime", "date", "time"]:
            return True
        datetime.datetime.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False


def is_null(value: Any) -> bool:
    return not value


def other_validator(value: Any) -> bool:
    return True


def is_list(value: Any) -> bool:
    return isinstance(value, list)


"""
Create a dictionary of the validator functions
"""
SIMPLE_VALIDATORS = {
    "date": is_date,
    "nullable": is_null,
    "other": other_validator,
    "list": is_list,
    "array": is_list,
}

COMPLEX_VALIDATORS = {
    "enum": is_valid_enum,
    "numeric": is_numeric,
    "string": is_string,
    "boolean": is_boolean
}


def get_validators(
        type_descriptor: Union[List[str], str],
        **kwargs):
    """
    For a given type definition (the ["string", "nullable"] bit), return
    the matching validator functions (the _is_x ones) as a list.
    """
    if not type(type_descriptor).__name__ == 'list':
        type_descriptor = [type_descriptor]  # type:ignore
    validators: List[Any] = []
    for descriptor in type_descriptor:
        if descriptor in COMPLEX_VALIDATORS:
            validators.append(COMPLEX_VALIDATORS[descriptor](**kwargs))
        else:
            validators.append(SIMPLE_VALIDATORS[descriptor])
    return validators


def field_validator(value, validators: list) -> bool:
    """
    Execute a set of validator functions (the _is_x) against a value.
    Return True if any of the validators are True.
    """
    return any([validator(value) for validator in validators])


class Schema():

    def __init__(self, definition: Union[dict, str]):
        """
        Compile a validator for a given schema.
        paramaters:
        - definition: a dictionary, text representation of a dictionary (JSON)
          or a JSON file containing a schema definition
        """
        # if we have a schema as a string, load it into a dictionary
        if type(definition).__name__ == 'str':
            if os.path.exists(definition):  # type:ignore
                definition = parse(open(definition, mode='r').read())  # type:ignore
            else:
                definition = parse(definition)  # type:ignore

        try:
            # read the schema and look up the validators
            self._validators = {
                item.get('name'): get_validators(
                        item['type'], 
                        symbols=item.get('symbols'), 
                        min=item.get('min', DEFAULT_MIN), # 64bit signed (not a limit, just a default)
                        max=item.get('max', DEFAULT_MAX),  # 64bit signed (not a limit, just a default)
                        format=item.get('format'))
                for item in definition.get('fields', [])  #type:ignore
            }
        except KeyError:
            raise ValueError("Invalid type specified in schema - valid types are: string, numeric, date, boolean, nullable, list, enum")
        if len(self._validators) == 0:
            raise ValueError("Invalid schema specification")

    def validate(self, subject: dict = {}, raise_exception=False) -> bool:

        result = True
        self.last_error = ''
 
        for key, value in self._validators.items():
            if not field_validator(subject.get(key), self._validators.get(key, [other_validator])):
                result = False
                for v in value:
                    self.last_error += f"'{key}' ({subject.get(key)}) did not pass validator {str(v)}.\n"
        if raise_exception and not result:
            raise ValueError(F"Record does not conform to schema - {self.last_error}. ")
        return result

    def __call__(self, subject: dict = {}, raise_exception=False) -> bool:
        # wrap the validate function
        return self.validate(subject=subject, raise_exception=raise_exception)
