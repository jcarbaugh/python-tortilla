# Tortilla

A Python library for dipping into [Salsa](http://www.salsalabs.com).

** PROTOTYPE **

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

    from tortilla.core import Supporter

    a_person = Supporter.get(123456)
    a_person.Email = 'me+stillme@notsalsa.com'
    a_person.save(fields='Email')

The exact API is still undetermined.

## Object definitions and fields

Salsa provides endpoints for inspecting the structure of object tables.

    field_defs = salsa.describe(Supporter.object)

Field objects can be created from the definitions

    from tortilla import fields
    supporter_fields = fields.get_fields(field_defs)

The field objects have methods for validating input and marshalling data.