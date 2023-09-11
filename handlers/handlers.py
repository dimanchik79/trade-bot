from keyboards.keyboards import *        
from states.states import *
from database.models import History


@bot.message_handler(content_types=["text"])
def message_users(message) -> None:
    """Отслеживание текстовых сообщений пользователя"""
    if filter_unregistred_users(message) == True:
        bot.reply_to(message, "Вы не можете писать сообщения. Зарегистрируйстсь, набрав команду /start")
        return       
    text_msg = message.text.lower().replace("!", "").replace(".", "")
    if text_msg in ["привет", "приветик", "приветствую", "здрасьте", "здорова", "здравствуйте", "hello"]:
        bot.reply_to(message, "И я Вас горячо приветствую!")
    else:
        bot.reply_to(message, "Я Вас не понимаю! Мой A.I. весьма ограничен(")
    History.create(chat_id=message.chat.id, 
                       user_name=message.chat.username, 
                       date=str(datetime.now()),
                       command = message.text,
                       result = "text message")
