# typhaon: python data validator


## What Is It?

Tests a dictionary for conformity against a schema.

The schema format is based on the schema used by Avro.

## How Do I Use It?

A schema is loaded into a _Schema_ object, data objects are then passed to the 'validate' method. 'validate' will return 'true' if the data conforms, non-conformity returns 'false', or can be set to raise an exception. On failure, the 'last_error' attribute is set to provide more information about the failure.

## Supported Types  

**string** - a character sequence  
Parameters
  - **format** - (optional) A Regular Expression to Match  

**numeric** - a number  
Paramters 
  - **min** - (optional) minimum valid value
  - **max** - (optional) maximum valid value

**date** - an iso format date or time  
No Parameters  

**boolean** - binary value  
Parameters
  - **symbols** - (optiona) list of valid values

**nullable** - empty or missing value allowed  
No Parameters

**list** - list of values  
No Parameters

**enum** - one of a list of values
Parameters

  -  **symbols** - (optional) list of valid values

**other** - not one of the above, but a required field  
No Parameters

### Example Schema
~~~json
{
 "fields": [
     {"name": "id",    "type": "string"},
     {"name": "name",  "type": "string"},
     {"name": "age",   "type": ["numeric", "null"], "min": 0},
     {"name": "color", "type": "enum", "symbols": ['RED', 'GREEN', 'BLUE']}
 ]
}
~~~

A field can be tested against multiple Types by putting the Types in a list (see _age_ in the Example Schema above). In this case the field is valid if any of the types match; this is most useful for values which are _null_ or a value.

The _null_ checker is valid if the field is _None_ or is a [Python False](https://docs.python.org/2.4/lib/truth.html)


### Example Code
~~~python
from typhaon import Schema

schema = Schema({"fields": [{"name": "string_field", "type": "string"}]})
data = {"name":"validator"}

is_valid = schema.validate(data)

if not is_valid:
    print(schema.last_error)
~~~

## How Do I Get It?
~~~
pip install git+https://github.com/joocer/Typhaon
~~~
or in your requirements.txt
~~~
git+https://github.com/joocer/Typhaon
~~~
