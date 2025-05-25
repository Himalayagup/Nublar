from database.base import Model, IntegerField, CharField

class Student(Model):
    id = IntegerField(primary_key=True)
    name = CharField(100)