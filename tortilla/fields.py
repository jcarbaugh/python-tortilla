import datetime

BLOB = 'blob'
DATETIME = 'datetime'
ENUM = 'enum'
FLOAT = 'float'
INT = 'int'
TIMESTAMP = 'timestamp'
TINYINT = 'tinyint'
VARCHAR = 'varchar'

class Field(object):

    def __init__(self, dfn):
        self._value = None
        self.name = dfn['name']
        self.label = dfn['label']
        self.default = dfn['defaultValue']
        self.is_nullable = dfn['nullable'] == '1'
        self.set(self.default)

    def __repr__(self):
        return u"<%s %s=%s>" % (self.__class__.__name__, self.name, self._value)

    def clean_value(self, value):
        if value == '' and self.is_nullable:
            return None
        return value

    def get(self):
        return self._value

    def set(self, value):
        self._value = self.clean_value(value)


class BlobField(Field):
    type = BLOB

class DateTimeField(Field):
    type = DATETIME

class EnumField(Field):
    type = ENUM

    def __init__(self, dfn):
        self.options = dfn['values']
        super(EnumField, self).__init__(dfn)

    def set(self, value):
        if value and value not in self.options:
            raise ValueError('%s is not a valid option' % value)
        super(EnumField, self).set(value)

class FloatField(Field):
    type = FLOAT

    def clean_value(self, value):
        value = super(FloatField, self).clean_value(value)
        if value:
            return float(value)
        elif value == '':
            return 0.0
        return None

class IntField(Field):
    type = INT

    def clean_value(self, value):
        value = super(IntField, self).clean_value(value)
        if value:
            return int(value)
        elif value == '':
            return 0
        return None

class TimestampField(Field):
    type = TIMESTAMP

class TinyIntField(IntField):
    type = TINYINT

class VarCharField(Field):
    type = VARCHAR

    def __init__(self, dfn):
        super(VarCharField, self).__init__(dfn)
        self.max_length = int(dfn['maxlength'])

FIELD_TYPES = {
    BLOB: BlobField,
    DATETIME: DateTimeField,
    ENUM: EnumField,
    FLOAT: FloatField,
    INT: IntField,
    TIMESTAMP: TimestampField,
    TINYINT: TinyIntField,
    VARCHAR: VarCharField,
}

def get_field(dfn, value=None):
    type = dfn.get('type')
    if type and type in FIELD_TYPES:
        field_class = FIELD_TYPES[type]
        field_obj = field_class(dfn)
        if value:
            field_obj.set(value)
        return field_obj

def get_fields(dfns, values=None):
    fields = []
    for dfn in dfns:
        field = get_field(dfn)
        if values and field.name in values:
            field.set(values[field.name])
        fields.append(field)
    return fields
