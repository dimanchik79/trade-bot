from telebot.handler_backends import State, StatesGroup
from loader import bot
from keyboards.keyboards import filter_unregistred_users
from database.routes import Routes
from config import TEXT_ONE

command = ''

class MyStates(StatesGroup):
    term_departure = State()
    term_destination = State()
    
    
@bot.message_handler(commands=['low', 'midle', 'high'])
def start_departure(message):
    global command
    """Обработка команд-состояний"""
    if filter_unregistred_users(message):
        return
    command = message.text
    bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
    bot.send_message(message.chat.id, TEXT_ONE)
 
    
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """Отмена ввода"""
    bot.send_message(message.chat.id, "Ввод отменен")
    bot.delete_state(message.from_user.id, message.chat.id)
    
    
@bot.message_handler(state=MyStates.term_departure)
def term_departure_get(message):
    """Запрос ввода станции отправления"""
    unique_adds = {}
    
    if message.text.isdigit() and len(message.text) == 7:
        for row in Routes.select().where(Routes.departure_station_id == f"{message.text}"):
            unique_adds[row.departure_station_name] = row.departure_station_id   
        if unique_adds == {}:
            bot.send_message(message.chat.id, "Такого кода не существует. Попробуйте еще")
            bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
            return
    elif message.text.isdigit() and len(message.text) != 7:
        bot.send_message(message.chat.id, "Код должен содержать только 7 цифр. Попробуйте еще")
        bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
        return

    elif message.text.isdigit() == False:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['term_departure'] = message.text
        for row in Routes.select().where(Routes.departure_station_name % f"*{data['term_departure']}*"):
            unique_adds[row.departure_station_name] = row.departure_station_id
        if unique_adds == {}:
            bot.send_message(message.chat.id, "Такой станции не нашлось. Попробуйте еще.")
            bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
            return
        else:
            msg = "<b>Вот уникальные коды станций:</b>\n"
            for key, value in unique_adds.items():
                    msg += f'{key} <i>{value}</i>\n'
            bot.send_message(message.chat.id, msg, parse_mode='html')
            bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
            return
    print(command, unique_adds)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['term_departure'] = message.text
    bot.send_message(message.chat.id, 'Введите код или название станции прибытия\n/cancel - отмена ввода')
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
    
    
    def unique_adds_check():
        pass