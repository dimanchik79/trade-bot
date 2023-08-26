from keyboards.keyboards import *

@bot.message_handler(content_types=["text"])
def message_users(message) -> None:
    """Отслеживание сообщений пользователя"""
    text_msg = message.text.lower().replace("!", "").replace(".", "")
    if text_msg in ["привет", "приветик", "приветствую", "здрасьте", "здорова", "здравствуйте", "hello"]:
        bot.reply_to(message, "И я Вас горячо приветствую!")
