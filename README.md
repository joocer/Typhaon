# typhaon: python data validator

## What Is It?
Tests conformity of a dictionary against a schema.

## How Do I Use It?
Schemas are defined in dictionaries

### Example Schema
~~~
{
 "fields": [
     {"name": "id",    "type": "string"},
     {"name": "name",  "type": "string"},
     {"name": "age",   "type": ["numeric", "null"]},
     {"name": "color", "type": "enum", symbols: ['RED', 'GREEN', 'BLUE']}
 ]
}
~~~

### Supported Types  

**string** - a character sequence  
**numeric** - a number  
**int** - alias for _numeric_  
**date** - an iso format date or time  
**boolean** - binary value (true/false, on/off, yes/no)  
**null** - None values allowed  
**nullable** - alias for _null_  
**list** - list of values  
**array** - alias for _list_
**enum** - one of a list of values !! enums require the set of valid values to be set in a _symbols_ list.  
**other** - not one of the above, but a required field  

A field can be tested against multiple Types by putting the Types in a list (see _age_ in the Example Schema above). In this case the field is valid if any of the types match; this is most useful for values which are _null_ or a value.

The _null_ checker is valid if the field is _None_ or is a [Python False](https://docs.python.org/2.4/lib/truth.html)

### Example Code
~~~python
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
