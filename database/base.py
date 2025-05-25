class Field:
    def __init__(self, field_type, primary_key=False, null=False, default=None, unique=False):
        self.type = field_type
        self.primary_key = primary_key
        self.null = null
        self.default = default
        self.unique = unique

class IntegerField(Field):
    def __init__(self, primary_key=False, null=False, default=None, unique=False):
        super().__init__("INTEGER", primary_key=primary_key, null=null, default=default, unique=unique)

class CharField(Field):
    def __init__(self, max_length=255, null=False, default=None, unique=False):
        super().__init__(f"VARCHAR({max_length})", null=null, default=default, unique=unique)
        self.max_length = max_length

class TextField(Field):
    def __init__(self, null=False, default=None, unique=False):
        super().__init__("TEXT", null=null, default=default, unique=unique)

class BooleanField(Field):
    def __init__(self, null=False, default=None, unique=False):
        super().__init__("BOOLEAN", null=null, default=default, unique=unique)

class DateTimeField(Field):
    def __init__(self, null=False, default=None, unique=False):
        super().__init__("DATETIME", null=null, default=default, unique=unique)

class DateField(Field):
    def __init__(self, null=False, default=None, unique=False):
        super().__init__("DATE", null=null, default=default, unique=unique)

class FloatField(Field):
    def __init__(self, null=False, default=None, unique=False):
        super().__init__("FLOAT", null=null, default=default, unique=unique)

class DecimalField(Field):
    def __init__(self, max_digits=10, decimal_places=2, null=False, default=None, unique=False):
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        super().__init__(f"DECIMAL({max_digits},{decimal_places})", null=null, default=default, unique=unique)

class ForeignKey(Field):
    def __init__(self, to, null=False, default=None, unique=False, on_delete="CASCADE"):
        # 'to' is a reference to the related model class or string
        self.to = to
        self.on_delete = on_delete
        super().__init__("INTEGER", null=null, default=default, unique=unique)  # FK typically stored as INTEGER id

class AutoField(IntegerField):
    def __init__(self):
        super().__init__(primary_key=True)

# Meta class to collect fields
class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != "Model":
            fields = {k: v for k, v in attrs.items() if isinstance(v, Field)}
            attrs["_meta"] = {"fields": fields}
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    pass
