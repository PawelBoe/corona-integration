import datetime

from peewee import IntegerField, FloatField, DateField, DateTimeField, CharField

from models.BaseModel import BaseModel


class CountryData(BaseModel):
    class Meta:
        table_name = "country_data"

    country_name = CharField()
    country_code = CharField()
    population = IntegerField()
    area = FloatField()
    population_density = FloatField()

    processed = DateTimeField(default=datetime.datetime.now)
