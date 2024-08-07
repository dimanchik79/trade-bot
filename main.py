import threading
from os import path
from utils.utils import *
import database.models
from telebot import custom_filters


def start_bot() -> None:
    """Функция запускает бота и иницилизирует фильтры состояний бота"""
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)


def main() -> None:
    """Функция запускает GUI и бота в отдельном потоке""" 
    window = MainWindow()
    threading.Thread(target=start_bot, args=(), daemon=True).start()
    window.window_show()

    
if __name__ == "__main__":
    if not path.exists('database/bot_base.db'):
        database.models.CurrentUser.create_table()
        database.models.History.create_table()
    main()
