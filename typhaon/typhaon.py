"""
Schema Validation

Tests a dictionary against a schema to test for conformity.
Schema definition is similar to - but not the same as - avro schemas
Supported Types:
    - string - a character sequence
    - numeric - a number
    - int - alias for numeric
    - date - an iso format date or time
    - boolean - binary value (true/false, on/off, yes/no)
    - other - not one of the above, but a required field
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

VALID_BOOLEAN_VALUES = ("true", "false", "on", "off", "yes", "no")


def _is_string(value):
    return type(value).__name__ == "str"


def _is_boolean(value):
    return str(value).lower() in VALID_BOOLEAN_VALUES


def _is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def _is_date(value):
    try:
        if type(value).__name__ in ["datetime", "date", "time"]:
            return True
        datetime.datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def _is_null(value):
    return value is None


def _other_validator(value):
    return True


def _not_valid(value):
    return False


VALIDATORS = {
    "string": _is_string,
    "numeric": _is_numeric,
    "int": _is_numeric,      # for compatibility only
    "date": _is_date,
    "boolean": _is_boolean,
    "null": _is_null,
    "nullable": _is_null,
    "not_specified": _not_valid,
    "other": _other_validator,
}


def get_validators(type_descriptor):
    if not type(type_descriptor).__name__ == 'list':
        type_descriptor = [type_descriptor]
    validators = []
    for descriptor in type_descriptor:
        validators.append(VALIDATORS[descriptor])
    return validators


def field_validator(value, validators):
    return any(
        [validator(value) for validator in validators]
        )


def validate(subject={}, schema={}):
    return schema.validate(subject)


class Schema():

    def __init__(self, definition):
        if type(definition).__name__ == 'str':
            definition = json.loads(definition)

        try:
            self._validators = {
                item.get('name'): get_validators(item['type'])
                for item in definition.get('fields', [])
            }
        except KeyError:
            raise ValueError("Invalid type specified in schema")

        if len(self._validators) == 0:
            raise ValueError("Invalid schema specification")

    def validate(self, subject=None, raise_exception=False):
        result = all(
            [field_validator(subject.get(key), self._validators.get(key, [_other_validator]))
                for key, value
                in self._validators.items()]
        )
        if raise_exception and not result:
            raise ValueError("Record does not conform to schema.")
        return result

    def __call__(self, subject=None, raise_exception=False):
        return self.validate(subject=subject, raise_exception=raise_exception)