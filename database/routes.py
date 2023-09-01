from peewee import *


DB = SqliteDatabase('database/routes.db')


class BaseModel(Model):
    class Meta:
        database = DB


class Routes(BaseModel):
    departure_station_id = IntegerField()
    departure_station_name = CharField(max_length=250)
    arrival_station_id = IntegerField()
    arrival_station_name = CharField(max_length=250)