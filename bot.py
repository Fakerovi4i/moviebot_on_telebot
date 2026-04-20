import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from config import BOT_TOKEN, #PROXY

# Для запуска прокси
# from config import PROXY
# from telebot import apihelper
# apihelper.proxy = {'https': PROXY}
# apihelper.READ_TIMEOUT = 60
# apihelper.CONNECT_TIMEOUT = 30


state_storage = StateMemoryStorage()


bot = telebot.TeleBot(BOT_TOKEN, threaded=True, skip_pending=True, state_storage=state_storage)


# Добавление фильтра состояний
bot.add_custom_filter(custom_filters.StateFilter(bot))

