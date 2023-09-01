from telebot.handler_backends import State, StatesGroup
from telebot import types
from loader import bot
from keyboards.keyboards import filter_unregistred_users
from database.routes import Routes



class MyStates(StatesGroup):
    term_departure = State()
    term_destination = State()
    
    
@bot.message_handler(commands=['low', 'midle', 'high'])
def start_departure(message):
    """Обработка команд-состояний"""
    if filter_unregistred_users(message):
        return
    bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
    bot.send_message(message.chat.id, 'Введите название станции отправления:\n/cancel - отмена ввода')
 
    
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """Отмена ввода"""
    bot.send_message(message.chat.id, "Ввод отменен")
    bot.delete_state(message.from_user.id, message.chat.id)
    
    
@bot.message_handler(state=MyStates.term_departure)
def term_departure_get(message):
    """Запрос ввода станции отправления"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['term_departure'] = message.text
    unique_adds = {}
    for row in Routes.select().where(Routes.departure_station_name % f"*{data['term_departure']}*"):
        unique_adds[row.departure_station_name] = row.departure_station_id
    if len(unique_adds) > 1:
        bot.send_message(message.chat.id, "Давайте уточним, конкретнее:\n")
        msg = ""
        for key, value in unique_adds.items():
                msg += f"{key} --- {value}\n"
        bot.send_message(message.chat.id, msg)
        bot.delete_state(message.from_user.id, message.chat.id)
        return
    bot.send_message(message.chat.id, 'Введите название станции назначения\n/cancel - отмена ввода')
    bot.set_state(message.from_user.id, MyStates.term_destination, message.chat.id)
 
 
@bot.message_handler(state=MyStates.term_destination)
def finish_get(message):
    """Запрос ввода станции назначения"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['term_destination'] = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"Departure: {data['term_departure']}\n"
               f"Destination: {data['term_destination']}\n</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)
    