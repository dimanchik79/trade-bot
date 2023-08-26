from peewee import *


DB = SqliteDatabase('database/bot_base.db')


class BaseModel(Model):
    class Meta:
        database = DB


class CurrentUser(BaseModel):
    chat_id = IntegerField()
    user_id = IntegerField()
    user_name = CharField(max_length=250)
    enter_date = DateTimeField()
    