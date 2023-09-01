from telebot.handler_backends import State, StatesGroup

class MyStates(StatesGroup):
    term_departure = State()
    term_destination = State()