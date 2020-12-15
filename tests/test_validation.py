"""
Validator Tests
"""
import datetime
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from typhaon import Schema


def test_validator_all_valid_values():

    TEST_DATA = { 
        "string_field": "string",
        "integer_field": 100,
        "boolean_field": True,
        "date_field": datetime.datetime.today(),
        "other_field": ["abc"],
        "nullable_field": None,
        "list_field": ['a', 'b', 'c'],
        "enum_field": "RED"
    }
    TEST_SCHEMA = {
        "fields": [
            {"name": "string_field",   "type": "string"},
            {"name": "integer_field",  "type": "numeric"},
            {"name": "boolean_field",  "type": "boolean"},
            {"name": "date_field",     "type": "date"},
            {"name": "other_field",    "type": "other"},
            {"name": "nullable_field", "type": "null"},
            {"name": "list_field",     "type": "list"},
            {"name": "enum_field",     "type": "enum",   "symbols": ['RED', 'GREEN', 'BLUE']}
        ]
    }

    test = Schema(TEST_SCHEMA)
    assert (test.validate(TEST_DATA))


def test_validator_invalid_string():

    TEST_DATA = { "string_field": 100 }
    TEST_SCHEMA = { "fields": [ { "name": "string_field", "type": "string" } ] }

    test = Schema(TEST_SCHEMA)
    assert (not test.validate(TEST_DATA))


def test_validator_invalid_number():

    TEST_DATA = { "number_field": "one hundred" }
    TEST_SCHEMA = { "fields": [ { "name": "number_field", "type": "numeric" } ] }

    test = Schema(TEST_SCHEMA)
    assert (not test.validate(TEST_DATA))


def test_validator_invalid_schema():

    result = True
    try:
        Schema({"name": "string"})
    except:
        result = False
    assert (not result)
    

def test_validator_invalid_boolean():

    TEST_DATA = { "boolean_field": "not true" }
    TEST_SCHEMA = { "fields": [ { "name": "boolean_field", "type": "boolean" } ] }

    test = Schema(TEST_SCHEMA)
    assert (not test.validate(TEST_DATA))


def test_validator_multiple_types():

    TEST_DATA_1 = { "multi": "True" }
    TEST_DATA_2 = { "multi": True }
    TEST_DATA_3 = { "multi": None }
    TEST_SCHEMA = { "fields": [ { "name": "multi", "type": ["string", "boolean", "null"] } ] }

    test = Schema(TEST_SCHEMA)
    assert (test.validate(TEST_DATA_1))
    assert (test.validate(TEST_DATA_2))
    assert (test.validate(TEST_DATA_3))


def test_validator_nonnative_types():

    TEST_DATA = { 
        "integer_field": "100",
        "boolean_field": "True",
        "date_field": "2000-01-01T00:00:00.000",
        "nullable_field": ""
    }
    TEST_SCHEMA = {
        "fields": [
            { "name": "integer_field",  "type": "numeric" },
            { "name": "boolean_field",  "type": "boolean" },
            { "name": "date_field",     "type": "date"    },
            { "name": "nullable_field", "type": "null"    }
        ]
    }

    test = Schema(TEST_SCHEMA)
    assert (test.validate(TEST_DATA))


def test_validator_extended_schema():
    """
    Ensure the validator will ignore additional fields in the schema
    """
    TEST_DATA = { "string_field": "the" }
    TEST_SCHEMA = {
        "table": "this is a test schema",
        "fields": [ 
            { 
                "name": "string_field", 
                "type": "string", 
                "description": "character array", 
                "last_updated": datetime.datetime.today() 
            } 
        ] 
    }

    test = Schema(TEST_SCHEMA)
    assert (test.validate(TEST_DATA))


def test_validator_loaders():
    """
    Ensure dictionary, json and json files load
    """
    import json

    TEST_SCHEMA_DICT = {"fields": [{"name": "string_field", "type": "string"}]}
    TEST_SCHEMA_STRING = json.dumps(TEST_SCHEMA_DICT)
    TEST_SCHEMA_FILE = 'temp'

    open(TEST_SCHEMA_FILE, 'w').write(TEST_SCHEMA_STRING)

    failed = False
    try:
        test = Schema(TEST_SCHEMA_DICT)
        test.validate({"string_field": "pass"})
    except Exception:
        failed = True
    assert not failed, "load schema from dictionary"

    failed = False
    try:
        test = Schema(TEST_SCHEMA_STRING)
        test.validate({"string_field": "pass"})
    except Exception:
        failed = True
    assert not failed, "load schema from string"

    failed = False
    try:
        test = Schema(TEST_SCHEMA_FILE)
        test.validate({"string_field": "pass"})
    except Exception:
        failed = True
    assert not failed, "load schema from file"


def test_validator_list():

    INVALID_TEST_DATA = {"key": "not a list"}
    VALID_TEST_DATA = {"key": ["is", "a", "list"]}
    TEST_SCHEMA = {"fields": [{"name": "key", "type": "list"}]}

    test = Schema(TEST_SCHEMA)
    assert (not test.validate(INVALID_TEST_DATA))
    assert (test.validate(VALID_TEST_DATA))


def test_validator_enum():

    INVALID_TEST_DATA = {"key": "left"}
    VALID_TEST_DATA = {"key": "north"}
    TEST_SCHEMA = {"fields": [{"name": "key", "type": "enum", "symbols": ['north', 'south']}]}

    test = Schema(TEST_SCHEMA)
    assert (not test.validate(INVALID_TEST_DATA))
    assert (test.validate(VALID_TEST_DATA))


if __name__ == "__main__":
    test_validator_all_valid_values()
    test_validator_invalid_string()
    test_validator_invalid_number()
    test_validator_invalid_schema()
    test_validator_invalid_boolean()
    test_validator_multiple_types()
    test_validator_nonnative_types()
    test_validator_extended_schema()
    test_validator_loaders()
    test_validator_list()
    test_validator_enum()
