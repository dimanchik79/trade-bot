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
   
   
@bot.message_handler(commands=['help'])
def help_command(message) -> None:
    # # btn3 = types.InlineKeyboardButton('/low')
    # # btn4 = types.InlineKeyboardButton('/hight')
    # # btn5 = types.InlineKeyboardButton('/custom')
    # # btn6 = types.InlineKeyboardButton('/history')
    # # btn7 = types.InlineKeyboardButton('/leavebot')
    bot.send_message(message.chat.id, HELP_TEXT, parse_mode='html')

    
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'help':
       help_command(callback.message)