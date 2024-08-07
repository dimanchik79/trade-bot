import telebot
from config import TOKEN
from telebot.storage import StateMemoryStorage

# Иннициализируем бот
bot = telebot.TeleBot(TOKEN, state_storage=StateMemoryStorage())