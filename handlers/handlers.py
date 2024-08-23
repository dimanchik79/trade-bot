from keyboards.keyboards import *
from states.states import *
from database.models import History


@bot.message_handler(content_types=["text"])
def message_users(message) -> None:
    """Отслеживание текстовых сообщений пользователя"""
    if filter_unregistred_users(message):
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
                   command=message.text,
                   result="text message")

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_message(callback: object) -> None:
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
                History.create(chat_id=callback.message.chat.id,
                               user_name=callback.message.chat.username,
                               date=str(datetime.now())[:18],
                               command="/exit",
                               result=f"User {callback.message.chat.username} exit the chat")
                bot.send_message(chat_id, "Вы покинули бот...")
