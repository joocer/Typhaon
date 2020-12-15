"""
Schema Validation

Tests a dictionary against a schema to test for conformity.
Schema definition is similar to - but not the same as - avro schemas

Supported Types:
    - string - a character sequence
    - numeric - a number
    - int - alias for numeric
    - date - a datetime.date or an iso format date or time
    - boolean - a boolean or a binary value (true/false, on/off, yes/no)
    - other - not one of the above, but a required field
    - null - Python Falsy (None, 0, Empty String, etc)

Example Schema:
{
 "name": "Table Name",
 "fields": [
     {"name": "id", "type": "string"},
     {"name": "country",  "type": ["string", "null"]},
     {"name": "followers", "type": ["string", "null"]}
 ]
}
"""
import datetime
import json
from typing import List, Any, Union
import os


VALID_BOOLEAN_VALUES = ("true", "false", "on", "off", "yes", "no")


def _is_string(value: Any) -> bool:
    return type(value).__name__ == "str"


def _is_boolean(value: Any) -> bool:
    return str(value).lower() in VALID_BOOLEAN_VALUES


def _is_numeric(value: Any) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def _is_date(value: Any) -> bool:
    try:
        if type(value).__name__ in ["datetime", "date", "time"]:
            return True
        datetime.datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def _is_null(value: Any) -> bool:
    return not value


def _other_validator(value: Any) -> bool:
    return True


def _not_valid(value: Any) -> bool:
    return False


def _is_list(value: Any) -> bool:
    return isinstance(value, list)


class _is_valid_enum():

    def __init__(self, symbols: list):
        self.symbols = symbols

    def __call__(self, value: Any):
        return value in self.symbols

"""
Create a dictionary of the validator functions
"""
VALIDATORS = {
    "string": _is_string,
    "numeric": _is_numeric,
    "int": _is_numeric,      # alias
    "date": _is_date,
    "boolean": _is_boolean,
    "null": _is_null,
    "nullable": _is_null,   # alias
    "not_specified": _not_valid,
    "other": _other_validator,
    "list": _is_list,
    "array": _is_list
}


def get_validators(
        type_descriptor: Union[List[str], str],
        symbols: Union[None, list] = None) -> list:
    """
    For a given type definition (the ["string", "nullable"] bit), return
    the matching validator functions (the _is_x ones) as a list.
    """
    if not type(type_descriptor).__name__ == 'list':
        type_descriptor = [type_descriptor]  # type:ignore
    validators = []
    for descriptor in type_descriptor:
        if descriptor == 'enum':
            validators.append(_is_valid_enum(symbols)) # type:ignore
        else:
            validators.append(VALIDATORS[descriptor]) # type:ignore
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
                definition = json.load(open(definition, mode='r'))  # type:ignore
            else:
                definition = json.loads(definition)  # type:ignore

        try:
            # read the schema and look up the validators
            self._validators = {
                item.get('name'): get_validators(item['type'], item.get('symbols'))
                for item in definition.get('fields', [])  #type:ignore
            }
        except KeyError:
            raise ValueError("Invalid type specified in schema; string, numeric, date, boolean, null, list, enum")
        if len(self._validators) == 0:
            raise ValueError("Invalid schema specification")

    def validate(self, subject: dict = {}, raise_exception=False) -> bool:
        # check the test subject against all of the fields in the validator
        result = all(
            [field_validator(subject.get(key), self._validators.get(key, [_other_validator]))
                for key, value
                in self._validators.items()]
        )
        if not result:
            self.last_error = ''
            # the validator is fast, but it discards the failures, rerun to get the errors
            for key, value in self._validators.items():
                if not field_validator(subject.get(key), self._validators.get(key, [_other_validator])):
                    self.last_error += f"'{key}' did not pass validator"
        if raise_exception and not result:
            raise ValueError(F"Record does not conform to schema - {self.last_error}.")
        return result

    def __call__(self, subject: dict = {}, raise_exception=False) -> bool:
        # wrap the validate function
        return self.validate(subject=subject, raise_exception=raise_exception)