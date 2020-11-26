"""
Validator test cases

1) Valid schema and data
2) Valid schema, invalid string
3) Valid schema, invalid number
4) Invalid schema, no data
"""

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from typhaon import Schema


def test_operator_validator_case_one():
    # CASE ONE = ALL VALID VALUES
    CASE_ONE_DATA = { 
        "string_field": "string",
        "integer_field": 100,
        "boolean_field": True,
        "date_field": "2000-01-01T00:00:00.000",
        "other_field": ["abc"],
        "nullable_field": None
    }
    CASE_ONE_SCHEMA = {
        "fields": [
            { "name": "string_field",   "type": "string"  },
            { "name": "integer_field",  "type": "numeric" },
            { "name": "boolean_field",  "type": "boolean" },
            { "name": "date_field",     "type": "date"    },
            { "name": "other_field",    "type": "other"   },
            { "name": "nullable_field", "type": "null"    }
        ]
    }

    test = Schema(CASE_ONE_SCHEMA)
    result = test.validate(CASE_ONE_DATA)
    assert (result != None), "[CASE ONE - VALIDATOR] Validator failed testing well-formed data"
    print("[CASE ONE - VALIDATOR] Passed")


def test_operator_validator_case_two():
    # CASE TWO = INVALID STRING
    CASE_TWO_DATA = { "string_field": 100 }
    CASE_TWO_SCHEMA = { "fields": [ { "name": "string_field", "type": "string" } ] }

    test = Schema(CASE_TWO_SCHEMA)
    result = test.validate(CASE_TWO_DATA)
    assert (not result), "[CASE TWO - VALIDATOR] Validator failed testing invalid string"
    print("[CASE TWO - VALIDATOR] Passed")


def test_operator_validator_case_three():
    # CASE THREE = INVALID NUMBER
    CASE_THREE_DATA = { "number_field": "one hundred" }
    CASE_THREE_SCHEMA = { "fields": [ { "name": "number_field", "type": "numeric" } ] }

    test = Schema(CASE_THREE_SCHEMA)
    result = test.validate(CASE_THREE_DATA)
    assert (not result), "[CASE THREE - VALIDATOR] Validator failed testing invalid number"
    print("[CASE THREE - VALIDATOR] Passed")


def test_operator_validator_case_four():
    # CASE FOUR = INVALID SCHEMA
    result = True
    try:
        Schema()
    except:
        result = False
    assert (not result), "[CASE FOUR - VALIDATOR] Validator failed testing invalid schema"
    print("[CASE FOUR - VALIDATOR] Passed")
    

def test_operator_validator_case_five():
    # CASE FIVE = INVALID BOOLEAN
    CASE_FIVE_DATA = { "boolean_field": "not true" }
    CASE_FIVE_SCHEMA = { "fields": [ { "name": "boolean_field", "type": "boolean" } ] }

    test = Schema(CASE_FIVE_SCHEMA)
    result = test.validate(CASE_FIVE_DATA)
    assert (not result), "[CASE FIVE - VALIDATOR] Validator failed testing invalid boolean"
    print("[CASE FIVE - VALIDATOR] Passed")


test_operator_validator_case_one()
test_operator_validator_case_two()
test_operator_validator_case_three()
test_operator_validator_case_four()
test_operator_validator_case_five()