from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List, Dict, Any, Optional
from datetime import datetime



def main_menu_keyboard():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔍Поиск по названию", "🧩Поиск по фильтрам",)
    keyboard.add("📜История поиска", "⭐Топ 10")
    return keyboard


def list_films_keyboard(films: List[Dict[str, Any]], page: int = 1, items_on_page: int = 5) -> InlineKeyboardMarkup:
    '''Клавиатура с найденными фильмами'''

    keyboard = InlineKeyboardMarkup(row_width=1)

    start_index = (page - 1) * items_on_page
    end_index = start_index + items_on_page
    current_films = films[start_index:end_index]

    for index, film in enumerate(current_films, start=start_index+1):

        movie_name = film.get('name', film.get('alternativeName', 'Нет названия'))
        year = film.get('year', '-')
        film_genre = film.get('genres', [{'name': '-'}])[0].get('name', '-')
        country = film.get('countries', [{'name': '-'}])[0].get('name', '-')
        rating = film.get('rating', {})
        rating_value = None
        if isinstance(rating, dict):
            for value in rating.values():
                if value is not None and value != 0:
                    rating = round(value, 1)
                    rating_value = True
                    break
        if rating_value is None:
            rating = '0'

        keyboard.add(
            InlineKeyboardButton(
                f"{index}. 🎬{movie_name} | {film_genre} | {rating} | {country} | {year}",
                callback_data=f"film_{film['id']}"))

    navigation_buttons = []
    total_pages = (len(films) + items_on_page - 1) // items_on_page

    if page > 1:
        navigation_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"page_{page - 1}"))

    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton("▶️ Вперед", callback_data=f"page_{page + 1}"))

    if navigation_buttons:
        # Создаем временную клавиатуру с row_width=2 для навигации
        nav_keyboard = InlineKeyboardMarkup(row_width=2)
        nav_keyboard.add(*navigation_buttons)
        # Добавляем кнопки из nav_keyboard в основную клавиатуру
        for row in nav_keyboard.keyboard:
            keyboard.row(*row)

    keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu"))

    return keyboard


def filters_keyboard(selected_filters: Optional[Dict] = None) -> InlineKeyboardMarkup:
    """Клавиатура с фильтрами с установкой галочки"""

    if selected_filters is None:
        selected_filters = {}
    keyboard = InlineKeyboardMarkup(row_width=2)

    rating_text = "  Рейтинг ⭐"
    genre_text = "  Жанры 🎭"
    year_text = "  Задать год 📆"
    country_text = "  Страна 🇷🇺🇮🇹🇺🇸"

    if 'rating' in selected_filters:
        rating_text = "✅ " + rating_text
    if 'genre' in selected_filters:
        genre_text = "✅ " + genre_text
    if 'year_with' in selected_filters or 'year_to' in selected_filters:
        year_text = f"✅ {year_text}"
    if 'country' in selected_filters:
        country_text = "✅ " + country_text


    keyboard.add(
        InlineKeyboardButton(genre_text, callback_data="filters_genre"),
        InlineKeyboardButton(rating_text, callback_data="filters_rating"),
        InlineKeyboardButton(country_text, callback_data="filters_country"),
        InlineKeyboardButton(year_text, callback_data="filters_year"),
        InlineKeyboardButton("❌Выход", callback_data="filters_exit"),
        InlineKeyboardButton("👀Найти", callback_data="filters_find")

    )
    return keyboard


def choice_rating_keyboard():
    """Клавиатура выбора рейтинга от 5 до 10"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("⭐ 5", callback_data="rating_5"),
        InlineKeyboardButton("⭐ 6", callback_data="rating_6"),
        InlineKeyboardButton("⭐ 7", callback_data="rating_7"),
        InlineKeyboardButton("⭐ 8", callback_data="rating_8"),
        InlineKeyboardButton("⭐ 9", callback_data="rating_9")
    )
    return keyboard


def choice_genre_keyboard(selected_genre: List[str] = None) -> InlineKeyboardMarkup:
    """Клавиатура с жанрами с поддержкой многогалочного выбора"""

    if selected_genre is None:
        selected_genre = []

    keyboard = InlineKeyboardMarkup(row_width=2)
    genres = [
        ("🎬 Боевик", "genre_боевик"),
        ("😂 Комедия", "genre_комедия"),
        ("😱 Ужасы", "genre_ужасы"),
        ("🤤 Аниме", "genre_аниме"),
        ("🔫 Триллер", "genre_триллер"),
        ("🚀 Фантастика", "genre_фантастика"),
        ("🕵️ Детектив", "genre_детектив"),
        ("🐉 Фэнтези", "genre_фэнтези")
    ]

    buttons = []

    for name, callback_data in genres:
        genre_name = callback_data.split("_")[1]
        if genre_name in selected_genre:
            display_name = "✅ " + name
        else:
            display_name = name
        buttons.append(
            InlineKeyboardButton(text=display_name, callback_data=callback_data))

    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton("️◀️ Назад к фильтрам", callback_data="back_to_filters"))
    return keyboard


def choice_year_keyboard(year_with = None, year_to = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора года"""
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(f"Начало: {year_with} г.", callback_data="year_with"),
        InlineKeyboardButton(f"Конец: {year_to} г.", callback_data="year_to"),
        InlineKeyboardButton("✅ Готово", callback_data="year_done")

    )
    return keyboard


def year_keyboard_message():
    keyboard = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(f"{year}") for year in range(2012, datetime.now().year + 1)]
    keyboard.add(*buttons)

    return keyboard


def choice_country_keyboard(selected_country: List[str] = None) -> InlineKeyboardMarkup:
    """Клавиатура с странами с поддержкой многогалочного выбора"""
    if selected_country is None:
        selected_country = []

    keyboard = InlineKeyboardMarkup(row_width=2)

    countries = [
        ("🇷🇺 Россия", "country_Россия"),
        ("🇮🇹 Италия", "country_Италия"),
        ("🇺🇸 США", "country_США"),
        ("🇬🇧 Великобритания", "country_Великобритания"),
        ("🇯🇵 Япония", "country_Япония"),
        ("🇫🇷 Франция", "country_Франция"),
        ("🇩🇪 Германия", "country_Германия"),
        ("🇨🇳 Китай", "country_Китай")
    ]

    buttons = []
    for name, callback_data in countries:
        country_name = callback_data.split("_")[1]
        if country_name in selected_country:
            display_name = "✅ " + name
        else:
            display_name = name
        buttons.append(
            InlineKeyboardButton(text=display_name, callback_data=callback_data))

    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton("️◀️ Назад к фильтрам", callback_data="back_to_filters"))
    return keyboard


def back_to_list_main_menu_button() -> InlineKeyboardMarkup:
    """Кнопки 'Назад к списку фильмов' и 'Главное меню'"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("◀️ Назад к списку фильмов", callback_data="back_to_list"))
    keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu"))
    return keyboard



