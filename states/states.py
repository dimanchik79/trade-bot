from telebot.handler_backends import State, StatesGroup
from loader import bot
from keyboards.keyboards import filter_unregistred_users
from database.routes import Routes
from config import TEXT_ONE, TEXT_TWO, NAME_IMG, COST_LEVEL, VAGON
import requests
from config import URL
import os


command = ''


class MyStates(StatesGroup):
    term_departure = State()
    term_arrival = State()
    
class MyDirect(StatesGroup):
    direct_departure = State()


@bot.message_handler(commands=['low', 'mid', 'high'])
def start_departure(message: object) -> None:
    global command
    """Обработка команд-состояний"""
    if filter_unregistred_users(message):
        return
    command = message.text
    bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
    bot.send_message(message.chat.id, TEXT_ONE)
 
    
@bot.message_handler(state=MyStates.term_departure)
def term_departure_get(message: object) -> None:
    """Запрос ввода станции отправления"""
    unique_adds = get_unique_adds(message)
    if unique_adds == {}:
        bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
        return
    elif len(unique_adds) > 1:
        msg = "Давайте уточним:\n"
        for key, value in unique_adds.items():
            msg += f"{key} {value}\n"
        bot.send_message(message.chat.id, msg)
        bot.set_state(message.from_user.id, MyStates.term_departure, message.chat.id)
        return
    elif len(unique_adds) == 1:
        bot.send_message(message.chat.id, f"Станция отправления:\n")
        for key, value in unique_adds.items():
            bot.send_message(message.chat.id, f"{key} {value}")
             
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['term_departure'] = [value for value in unique_adds.values()]
        bot.send_message(message.chat.id, 'Введите код или название станции прибытия\n/cancel - отмена ввода')
        bot.set_state(message.from_user.id, MyStates.term_arrival, message.chat.id)
 
 
@bot.message_handler(state=MyStates.term_arrival)
def finish_get(message: object) -> None:
    """Запрос ввода станции назначения"""
    unique_adds = get_unique_adds(message)
    if unique_adds == {}:
         bot.set_state(message.from_user.id, MyStates.term_arrival, message.chat.id)
         return
    elif len(unique_adds) > 1:
        msg = "Давайте уточним:\n"
        for key, value in unique_adds.items():
            msg += f"{key} {value}\n"
        bot.send_message(message.chat.id, msg)
        bot.set_state(message.from_user.id, MyStates.term_arrival, message.chat.id)
        return
    elif len(unique_adds) == 1:
        bot.send_message(message.chat.id, f"Станция прибытия:\n")
        for key, value in unique_adds.items():
            bot.send_message(message.chat.id, f"{key} {value}")         
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['term_arrival'] = [value for value in unique_adds.values()]
    
    bot.delete_state(message.from_user.id, message.chat.id)
    unique_adds = {}
    for row in Routes.select().where((Routes.departure_station_id == f"{data['term_departure'][0]}") & 
                                     (Routes.arrival_station_id ==  f"{data['term_arrival'][0]}")):
        unique_adds[row.departure_station_name] = row.departure_station_id
        unique_adds[row.arrival_station_name] = row.arrival_station_id   
    if unique_adds == {}:
       bot.send_message(message.chat.id, "Увы! Но такого направления не найдено(")
       return
    stations =[]  
    for key, value in unique_adds.items():
        stations.extend([key, value])
    bot.send_message(message.chat.id, "Немножко подождем...")
   
    #Делаем запрос к серверу и парсим ответ 
    querystring = {'service': 'tutu_trains',
                'term': stations[1],
                'term2': stations[3]}
    parse = requests.get(URL, params=querystring)
    parse_text = parse.text
    parse = dict(parse.json())
    stations_count = parse_text.count("arrivalStation", 0)
    
    for count in range(stations_count):
        name = 'None' if parse['trips'][count]['name'] in ('', None) else parse['trips'][count]['name']
        departure_station = f"{find_station_name(parse['trips'][count]['departureStation'])} ({parse['trips'][count]['departureStation']})"
        arrival_station = f"{find_station_name(parse['trips'][count]['arrivalStation'])} ({parse['trips'][count]['arrivalStation']})"
        run_departure_station = f"{find_station_name(parse['trips'][count]['runDepartureStation'])} ({parse['trips'][count]['runDepartureStation']})"
        run_arrival_station = f"{find_station_name(parse['trips'][count]['runArrivalStation'])} ({parse['trips'][count]['runArrivalStation']})"
        departure_time = f"{parse['trips'][count]['departureTime']} (мск)"
        arrival_time = f"{parse['trips'][count]['arrivalTime']} (мск)"
        train_number = parse['trips'][count]['trainNumber']
        firm = "ДА" if parse['trips'][count]['firm'] else "НЕТ"
        travel_time = int(parse['trips'][count]['travelTimeInSeconds'])
        travel_time = convert(travel_time)
        categories = parse['trips'][count]['categories']
        cost = []
        for count in range(len(categories)):
           cost.append([categories[count]['price'], categories[count]['type']])
        cost = sorted(cost)                                   
        bot.send_photo(message.chat.id, photo=open(NAME_IMG[name], 'rb'))
        bot.send_message(message.chat.id, f"""<b>Имя поезда:</b> <i>{name if name != 'None' else 'БЕЗ НАЗВАНИЯ'}</i> 
<b>Номер поезда:</b> <i>{train_number}</i>
<b>Фирменный поезд:</b> <i>{firm}</i>
<b>Станция отправления:</b> <i>{departure_station}</i> 
<b>Станция прибытия:</b> <i>{arrival_station}</i>
<b>Время отправления:</b> <i>{departure_time}</i>
<b>Время прибытия:</b> <i>{arrival_time}</i>
<b>Время следования:</b> <i>{travel_time}</i> 
<b>Начальная станция:</b> <i>{run_departure_station}</i> 
<b>Конечная станция:</b> <i>{run_arrival_station}</i>\n 
<b>Цена билета в категории ({COST_LEVEL[f'{command}']}):</b> {get_cost(cost, command)}
        """, parse_mode="html")
        
    bot.delete_state(message.from_user.id, message.chat.id)
   
    
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message: object) -> None:
    """Отмена ввода"""
    global command
    command = message.text
    bot.send_message(message.chat.id, "Ввод отменен")
    bot.delete_state(message.from_user.id, message.chat.id)
    

@bot.message_handler(commands=['direct'])
def direct_departure(message: object) -> None:
    """Обработка команды-состояния direct"""
    if filter_unregistred_users(message):
        return
    global command
    command = message.text
    bot.set_state(message.from_user.id, MyDirect.direct_departure, message.chat.id)
    bot.send_message(message.chat.id, TEXT_TWO)


@bot.message_handler(state=MyDirect.direct_departure)
def direct_term_departure_get(message: object) -> None:
    """Запрос ввода станции отправления"""
    with open(f'direct{message.from_user.id}.txt', 'w') as file:
        for row in Routes.select().where(Routes.departure_station_name % f"*{message.text}*"):
            file.write(f"{row.departure_station_id} {row.departure_station_name} ---> {row.arrival_station_id} {row.arrival_station_name}\n")
    doc = open(f'direct{message.from_user.id}.txt', 'rb')
    bot.send_document(message.from_user.id, doc)
    doc.close()
    os.remove(f'direct{message.from_user.id}.txt')
    bot.delete_state(message.from_user.id, message.chat.id)
    

def get_unique_adds(msg: object) -> dict:
    """Функция проводит валидацию введенного кода станции"""
    unique_adds = {}   
    if msg.text.isdigit() and len(msg.text) == 7:
        for row in Routes.select().where(Routes.departure_station_id == f"{msg.text}"):
            unique_adds[row.departure_station_name] = row.departure_station_id   
        if unique_adds == {}:
            bot.send_message(msg.chat.id, "Такого кода не существует. Попробуйте еще")
            return {}
        else:
            return unique_adds    
   
    elif msg.text.isdigit() and len(msg.text) != 7:
        bot.send_message(msg.chat.id, "Код должен содержать только 7 цифр. Попробуйте еще")
        return {}
    
    elif msg.text.isdigit() == False:
        for row in Routes.select().where(Routes.departure_station_name % f"*{msg.text}*"):
            unique_adds[row.departure_station_name] = row.departure_station_id
        if unique_adds == {}:
            bot.send_message(msg.chat.id, "Такой станции не нашлось. Попробуйте еще.")
            return {}
        else:
            return unique_adds
        

def find_station_name(station_id: str) -> str:
    """Функция возвращает название станции по id"""
    for row in Routes.select().where(Routes.departure_station_id == f"{station_id}"):
        return f"{row.departure_station_name}"
    
 
def convert(seconds: int) -> str:
    """Функция преобразует время в секундах в hh:mm:ss"""
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hour, minutes, seconds)


def get_cost(diff_cost: list, comand_for: str) -> str:
    """Функция определят какую цену возвращать, в зависимости от команды"""
    print(diff_cost)
    if comand_for == "/low":
        return f"{VAGON[diff_cost[0][1]]}  - {diff_cost[0][0]} руб."
    if comand_for == "/high":
        return f"{VAGON[diff_cost[-1][1]]}  - {diff_cost[-1][0]} руб."
    if comand_for == "/mid":
        if len(diff_cost) < 3:
            txt = f"средней цены нет. Вывожу самую низкую - {diff_cost[0][0]} руб."
        for count in range(1, len(diff_cost) - 1):
            txt = f"{VAGON[diff_cost[count][1]]}  - {diff_cost[count][0]} руб.\n"
        return txt