from peewee import Model, SqliteDatabase

db = SqliteDatabase('data/data.sqlite')


class BaseModel(Model):
    class Meta:
        database = db
