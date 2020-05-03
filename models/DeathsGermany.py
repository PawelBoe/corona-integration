import datetime

from peewee import IntegerField, DateField, DateTimeField, CharField

from models.BaseModel import BaseModel


class DeathsGermany(BaseModel):
    class Meta:
        table_name = "deaths_germany"

    date = DateField()
    age_group_start = IntegerField()
    age_group_end = IntegerField()
    deaths = IntegerField()

    processed = DateTimeField(default=datetime.datetime.now)
