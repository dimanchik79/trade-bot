import telebot
from config import *
from telebot.storage import StateMemoryStorage


bot = telebot.TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())