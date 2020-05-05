import datetime

from peewee import IntegerField, DateField, DateTimeField

from models.BaseModel import BaseModel


class RkiTests(BaseModel):
    class Meta:
        table_name = "rki_tests"

    calendar_week = IntegerField()
    tests = IntegerField()
    positives = IntegerField()
    participating_laboratories = IntegerField()

    processed = DateTimeField(default=datetime.datetime.now)
