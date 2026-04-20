  # 🎬 Movie Search Bot


[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/Fakerovi4i/moviebot_on_telebot)

Умный Telegram-бот для поиска фильмов и сериалов через [Kinopoisk API](https://kinopoiskapiunofficial.tech/).

Поддерживает поиск по названию и **сложные фильтры** с множественным выбором.

### ✨ Возможности
- Поиск фильма по названию (универсальный обработчик текста)
- Расширенный поиск по фильтрам:
  - Жанры (множественный выбор с галочками)
  - Страны (множественный выбор)
  - Рейтинг и диапазон года
- Пагинация результатов
- История поиска пользователя
- Просмотр Топ-100 фильмов
- Красивые динамические клавиатуры

### 🛠 Технологии
- **Python 3.12** + **pyTelegramBotAPI (telebot)**
- Finite State Machine (StatesGroup)
- Kinopoisk Unofficial API
- Динамическое формирование inline-клавиатур

### ⚡ Сложности и решения
- Множественные фильтры с визуальными галочками → динамическое обновление клавиатур в реальном времени
- Сложная логика состояний (фильтры → пагинация → просмотр) → грамотная работа с `retrieve_data`
- Большой объём данных → реализовал пагинацию и оптимизированный вывод

### 🚀 Запуск
```bash
git clone https://github.com/Fakerovi4i/moviebot_on_telebot.git
cd moviebot_on_telebot
pip install -r requirements.txt

# Создай файл .env и вставь туда свои токены
cp .env.example .env
```

После этого запусти бота:
```bash
python main.py