# typhaon: python data validator

## What Is It?
Tests a dictionary against a schema to test for conformity.

## How Do I Use It?
Schemas are defined in dictionaries

Example Schema:
~~~
{
 "name": "Data Set Name",
 "fields": [
     {"name": "id",   "type": "string"},
     {"name": "name", "type": "string"},
     {"name": "age",  "type": ["numeric", "null"]}
 ]
}
~~~

Supported Types:  
    - **string** - a character sequence  
    - **numeric** - a number  
    - **int** - alias for numeric  
    - **date** - an iso format date or time  
    - **boolean** - binary value (true/false, on/off, yes/no)  
    - **null** - None values allowed  
    - **other** - not one of the above, but a required field  


## How Do I Get It?
~~~
pip install git+https://github.com/joocer/Typhaon
~~~
or in your requirements.txt
~~~
git+https://github.com/joocer/Typhaon
~~~
