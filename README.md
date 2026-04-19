# Movie Search Bot

Telegram бот для поиска фильмов через Kinopoisk API.

## Команды

- `/start` — перезапуск
- `/search` — поиск по названию
- `/filters` — поиск по фильтрам
- `/top` — топ‑100
- `/history` — история просмотров


## Требования

- Python 3.8+
- Telegram Bot Token (от [@BotFather](https://t.me/BotFather))
- API‑ключ [Kinopoisk API Dev](https://kinopoiskapiunofficial.tech/)


## Установка

1. `pip install -r requirements.txt`
2. Создать `.env` с полями:
- BOT_TOKEN=токен_бота
- SITE_API_KEY=ключ_Kinopoisk_api