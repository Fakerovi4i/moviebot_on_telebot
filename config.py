import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SITE_API_KEY = os.getenv("SITE_API_KEY")
API_HOST = "https://api.kinopoisk.dev/v1.4"
API_TIMEOUT = 30

# PROXY = os.getenv("PROXY")

