from peewee import *

# Definē datubāzi
db = SqliteDatabase(None)


# Datu modelis
class DataModel(Model):
    column1 = CharField()
    column2 = CharField()
    value = FloatField()

    class Meta:
        database = db
