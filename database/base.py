# models/base.py
class Field:
    def __init__(self, field_type, primary_key=False):
        self.type = field_type
        self.primary_key = primary_key

class IntegerField(Field):
    def __init__(self, primary_key=False):
        super().__init__("INTEGER", primary_key=primary_key)

class CharField(Field):
    def __init__(self, max_length=255):
        super().__init__(f"VARCHAR({max_length})")

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != "Model":
            fields = {k: v for k, v in attrs.items() if isinstance(v, Field)}
            attrs["_meta"] = {"fields": fields}
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    pass
