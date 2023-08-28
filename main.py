import threading
from os import path
from handlers.handlers import *
from loader import *
from utils.utils import *
import database.models


def start_bot() -> None:
    bot.polling(none_stop=True)


def main() -> None:
    window = MainWindow()
    threading.Thread(target=start_bot, args=(), daemon=True).start()
    window.window_show()

    
if __name__ == "__main__":
    if not path.exists('database/bot_base.db'):
        database.models.CurrentUser.create_table()
    main()
