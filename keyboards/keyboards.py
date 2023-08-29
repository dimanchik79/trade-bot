from loader import bot
from database.models import CurrentUser
from datetime import datetime
from telebot import types
from config import HELP_TEXT


@bot.message_handler(commands=['start'])
def users_registtration(message) -> None:
    """Обработка команды /start. Регистрация новых пользователей бота"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Вывести справку по командам бота?', callback_data="help"))
    user = [name for name in CurrentUser.select().where(CurrentUser.user_id == user_id)]
    if user != []:
        bot.send_message(chat_id, f"С возвращением, <b>{user_name}</b>!!!", parse_mode='html', reply_markup=markup)
    else:
        CurrentUser.create(chat_id=chat_id, user_id=user_id, user_name=user_name, enter_date=str(datetime.now()))
        bot.send_message(chat_id, f"Привет, <b>{user_name}</b>!!! Ваш ID {user_id}", parse_mode='html')
        bot.send_message(chat_id, f"и Вы успешно зарегистрированы в системе!", parse_mode='html', reply_markup=markup)

 
@bot.message_handler(commands=['leavebot'])
def users_registtration(message) -> None:
    """Обработка команды leavebot"""
    markup = types.InlineKeyboardMarkup()
    btn_no = types.InlineKeyboardButton('Нет', callback_data="no_exit")
    btn_yes = types.InlineKeyboardButton('Да', callback_data="yes_exit")
    markup.add(btn_no, btn_yes)
    bot.send_message(message.chat.id, f"Вы действительно желаете покинуть бот?", reply_markup=markup)

   
@bot.message_handler(commands=['help'])
def help_command(message) -> None:
    """Обработка команды help"""
    if filter_unregistred_users(message):
        return
    bot.send_message(message.chat.id, HELP_TEXT, parse_mode='html')

    
@bot.callback_query_handler(func=lambda callback: True) 
def callback_message(callback) -> None:
    """Callbacks на кнопки"""
    if callback.data == 'help':
        help_command(callback.message)
    if callback.data == 'no_exit':
        bot.send_message(callback.message.chat.id, "Мудрое решение!")
    if callback.data == 'yes_exit':
        chat_id = callback.message.chat.id
        if filter_unregistred_users(callback.message):
            return
        else:
            CurrentUser.get(CurrentUser.chat_id == chat_id).delete_instance()
            bot.send_message(chat_id, "Вы покинули бот...") 


def filter_unregistred_users(msg) -> bool:
    """Функция определяет зарегистрирован ли пользовтель или нет"""
    chat_id = msg.chat.id
    user = [name for name in CurrentUser.select().where(CurrentUser.chat_id == chat_id)]
    if user == []:
        bot.send_message(chat_id, "Вы не зарегистрированы в системе.\nВыполните команду /start")
        return True
    else:
        return False        