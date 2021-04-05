import datetime

from peewee import IntegerField, DateField, DateTimeField, CharField

from models.BaseModel import BaseModel


class CoronaCasesWeekly(BaseModel):
    class Meta:
        table_name = "corona_cases_weekly"

    date_reported = DateField()
    year = IntegerField()
    week = IntegerField()
    cases = IntegerField()
    deaths = IntegerField()
    country_code = CharField()
    population = IntegerField()
    continent = CharField()

    processed = DateTimeField(default=datetime.datetime.now)
