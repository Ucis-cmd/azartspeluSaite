from peewee import *

db = SqliteDatabase(None)

class GadaModelis(Model):
    gads = IntegerField()
    pavisam = FloatField()
    automāti = FloatField()
    kazino_galdi = FloatField()
    bingo_spēles = FloatField()
    totalizatori = FloatField()
    interaktīvās_spēles = FloatField()
    tālrunis = FloatField()

    class Meta:
        database = db
