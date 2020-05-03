import datetime

from peewee import IntegerField, DateField, DateTimeField, CharField

from models.BaseModel import BaseModel


class CoronaCases(BaseModel):
    class Meta:
        table_name = "corona_cases"

    date_reported = DateField()
    day = IntegerField()
    month = IntegerField()
    year = IntegerField()
    cases = IntegerField()
    deaths = IntegerField()
    country = CharField()
    geo_id = CharField()
    country_code = CharField()
    population = IntegerField()
    continent = CharField()

    processed = DateTimeField(default=datetime.datetime.now)
