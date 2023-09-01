import telebot
from config import *
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()

bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)