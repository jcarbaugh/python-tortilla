# Tortilla

A Python library for dipping into [Salsa](http://www.salsalabs.com).

** PROTOTYPE **

This is still very much a work in progress. I'm not sure what the final structure of this library will be; I've got a number of ideas floating around in the repo here. [I'm open to suggestions!](https://github.com/sunlightlabs/python-tortilla/issues)

## The Basic Client

Authentication

    from tortilla.core import salsa
    salsa.authenticate('salsa20XX', 'me@notsalsa.com', 'asecurepassword')

Save a new supporter

    salsa.save('supporter', {'Email': 'me@notsalsa.com'})

Updating a supporter

    salsa.save('supporter', {'First_Name': 'Tomatillo'}, key=123456)

## Salsa Objects

There are Salsa objects that are meant to sit atop the underlying client methods.

    a_person = salsa.supporter('123456')
    a_person.Email = 'me+stillme@notsalsa.com'
    salsa.save(a_person)

The exact API is still undetermined.

## Object definitions and fields

Salsa provides endpoints for inspecting the structure of object tables.

    field_defs = salsa.describe(Supporter.object)

Field objects can be created from the definitions

    from tortilla import fields
    supporter_fields = fields.get_fields(field_defs)

The field objects have methods for validating input and marshalling data.