from loader import bot
from database.models import CurrentUser
from datetime import datetime


@bot.message_handler(commands=['start'])
def command_users(message) -> None:
    """Отправка сообщений по команде пользователя /start"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user = [name for name in CurrentUser.select().where(CurrentUser.user_id == user_id)]
    if user != []:
        bot.send_message(chat_id, f"С возвращением, <b>{user_name}</b>!!!", parse_mode='html')
    else:
        CurrentUser.create(chat_id=chat_id, user_id=user_id, user_name=user_name, enter_date=str(datetime.now()))
        bot.send_message(chat_id, f"Привет, <b>{user_name}</b>!!! Ваш ID {user_id}", parse_mode='html')
        bot.send_message(chat_id, f"и Вы успешно зарегистрированы в системе!", parse_mode='html')