import datetime

from peewee import IntegerField, DateField, DateTimeField

from models.BaseModel import BaseModel


class DiviBeds(BaseModel):
    class Meta:
        table_name = "civi_beds"

    date = DateField()
    used_beds = IntegerField()
    free_beds = IntegerField()
    corona_beds = IntegerField()
    emergency_beds = IntegerField()

    processed = DateTimeField(default=datetime.datetime.now)
