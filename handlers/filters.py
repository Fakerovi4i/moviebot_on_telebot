"""
Все обработчики, связанные с поиском по фильтрам (ChoiceFilters).
"""

import logging
from datetime import datetime
from telebot.types import Message, CallbackQuery

from bot import bot
from api_requests import find_movies_by_filters
from keyboards import (
    filters_keyboard,
    choice_rating_keyboard,
    choice_genre_keyboard,
    choice_country_keyboard,
    choice_year_keyboard,
    year_keyboard_message,
    main_menu_keyboard,
    list_films_keyboard
)
from my_states import ChoiceFilters, Pagination

logger = logging.getLogger(__name__)

# ====================== ОСНОВНОЕ МЕНЮ ФИЛЬТРОВ ======================
@bot.message_handler(func=lambda message: message.text in ['/filters', '🧩Поиск по фильтрам'])
def filters(message: Message):
    logger.info("Пользователь %s открыл меню фильтров", message.from_user.id)
    try:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)

        bot.set_state(message.from_user.id, ChoiceFilters.waiting_filters, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data.clear()

        bot.send_message(
            message.chat.id,
            "Выберите фильтр:",
            reply_markup=filters_keyboard())

    except Exception as e:
        logger.exception("Ошибка при запуске меню фильтров")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка. Попробуйте позже.",
            reply_markup=main_menu_keyboard()
        )

# ====================== РЕЙТИНГ ======================
@bot.callback_query_handler(func=lambda call: call.data == "filters_rating", state=ChoiceFilters.waiting_filters)
def callback_rating_filter(call):
    """ Обработчик нажатия на кнопки рейтинга """
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "🍿 Выбери минимальный рейтинг:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=choice_rating_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("rating_"), state=ChoiceFilters.waiting_filters)
def callback_rating_selected(call: CallbackQuery):
    """ Обработчик выбора рейтинга """
    bot.answer_callback_query(call.id)
    rating = call.data.split("_")[1]

    # Сохраняем выбранный рейтинг в состояние
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['rating'] = rating
        selected_filters = dict(data)

    bot.edit_message_text(
        f"Выбрано: ⭐ {rating}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=filters_keyboard(selected_filters=selected_filters)
    )
    logger.info("Пользователь %s выбрал рейтинг: %s", call.from_user.id, rating)

# ====================== ГОД ======================
@bot.callback_query_handler(func=lambda call: call.data == "filters_year", state=ChoiceFilters.waiting_filters)
def callback_year_filter(call):
    """ Обработчик кнопки фильтров по году """
    bot.answer_callback_query(call.id)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        year_with = data.get('year_with', '1985')
        year_to = data.get('year_to', str(datetime.now().year))

    bot.edit_message_text(
        "🍿 Выбери диапазон:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=choice_year_keyboard(year_with=int(year_with), year_to=int(year_to))
    )

@bot.callback_query_handler(func=lambda call: call.data == "year_with", state=ChoiceFilters.waiting_filters)
def callback_year_with(call: CallbackQuery):
    """Обработчик кнопки начала диапазона года"""
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "Выберете из списка или введите свой: 📆",
        reply_markup=year_keyboard_message()
    )
    bot.set_state(call.from_user.id, ChoiceFilters.waiting_year_with, call.message.chat.id)

@bot.message_handler(state=ChoiceFilters.waiting_year_with)
def choice_year_with(message: Message):
    """Обработчик начала диапазона года"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        selected_filters = dict(data)
        year_to = data.get('year_to', str(datetime.now().year))

    year_with = message.text.strip()

    if not year_with.isdigit() or int(year_with) > int(year_to):
        bot.send_message(
            message.chat.id,
            f"⚠️ Некорректный ввод!\nГод должен быть числом от 0 до {year_to}",
            reply_markup=filters_keyboard(selected_filters)
        )
        bot.set_state(message.from_user.id, ChoiceFilters.waiting_filters, message.chat.id)
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['year_with'] = year_with
        data['year_to'] = year_to

    bot.delete_message(message.chat.id, message.message_id)
    bot.set_state(message.from_user.id, ChoiceFilters.waiting_filters, message.chat.id)

    bot.send_message(
        message.chat.id,
        f"Выбрано: {year_with}",
        reply_markup=choice_year_keyboard(year_with=int(year_with), year_to=int(year_to)))


@bot.callback_query_handler(func=lambda call: call.data == "year_to", state=ChoiceFilters.waiting_filters)
def callback_year_to(call):
    """Обработчик кнопки конца диапазона года"""
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "Выберете из списка или введите свой: 📆",
        reply_markup=year_keyboard_message()
    )
    bot.set_state(call.from_user.id, ChoiceFilters.waiting_year_to, call.message.chat.id)

@bot.message_handler(state=ChoiceFilters.waiting_year_to)
def choice_year_to(message: Message):
    """Обработчик конца диапазона года"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        selected_filters = dict(data)
        year_with = data.get('year_with', "1985")

    year_to = message.text.strip()

    if not year_to.isdigit() or int(year_to) < int(year_with):
        bot.send_message(
            message.chat.id,
            f"⚠️ Некорректный ввод!\nГод должен быть числом до {datetime.now().year}",
            reply_markup=filters_keyboard(selected_filters)
        )
        bot.set_state(message.from_user.id, ChoiceFilters.waiting_filters, message.chat.id)
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['year_to'] = year_to
        data['year_with'] = year_with

    bot.delete_message(message.chat.id, message.message_id)
    bot.set_state(message.from_user.id, ChoiceFilters.waiting_filters, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"Выбрано: {year_to}",
        reply_markup=choice_year_keyboard(year_with=int(year_with), year_to=int(year_to)))

@bot.callback_query_handler(func=lambda call: call.data == "year_done", state=ChoiceFilters.waiting_filters)
def callback_year_done(call):
    """Обработчик кнопки завершения выбора года"""
    bot.answer_callback_query(call.id)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        selected_filters = dict(data)

    bot.edit_message_text(
        "Выберете фильтры:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=filters_keyboard(selected_filters=selected_filters)
    )


# ====================== ЖАНРЫ ======================

@bot.callback_query_handler(func=lambda call: call.data == "filters_genre", state=ChoiceFilters.waiting_filters)
def callback_genre_filter(call):
    """ Обработчик кнопки Жанры """
    bot.answer_callback_query(call.id)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        selected_genre = data.get('genre', [])
    bot.edit_message_text(
        "🎭 Выбери жанры:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=choice_genre_keyboard(selected_genre)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"), state=ChoiceFilters.waiting_filters)
def callback_genre_selected(call):
    """Обработчик выбора/отмены жанра (галочки)"""
    bot.answer_callback_query(call.id)
    genre = call.data.split("_", 1)[1]

    # Сохраняем выбранный рейтинг в состояние
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        if 'genre' not in data:
            data['genre'] = []
        if genre in data['genre']:
            data['genre'].remove(genre)
        else:
            data['genre'].append(genre)
        selected_genre = data['genre']

    bot.edit_message_text(
        "Выбери жанры: 🎭",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=choice_genre_keyboard(selected_genre)
    )

# ====================== СТРАНЫ ======================
@bot.callback_query_handler(func=lambda call: call.data == "filters_country", state=ChoiceFilters.waiting_filters)
def callback_country_filter(call):
    """ Обработчик нажатия на кнопку Выбор страны """
    bot.answer_callback_query(call.id)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        selected_country = data.get('country', [])

    bot.edit_message_text(
        "🇷🇺🇮🇹🇺🇸 Выбери страну:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=choice_country_keyboard(selected_country)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"), state=ChoiceFilters.waiting_filters)
def callback_country_selected(call):
    """ Обработчик выбора/отмены страны (галочки) """
    bot.answer_callback_query(call.id)
    country = call.data.split("_", 1)[1]

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        if 'country' not in data:
            data['country'] = []
        if country in data['country']:
            data['country'].remove(country)
        else:
            data['country'].append(country)
        selected_country = data['country']

    bot.edit_message_text(
        "🇷🇺🇮🇹🇺🇸 Выбери страны:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=choice_country_keyboard(selected_country)
    )

# ====================== ЗАПУСК ПОИСКА ======================

@bot.callback_query_handler(func=lambda call: call.data == "filters_find", state=ChoiceFilters.waiting_filters)
def callback_find_movies(call: CallbackQuery):
    """Обработчик нажатия на кнопку Запуска поиска"""
    bot.answer_callback_query(call.id)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        filters_movie = data.copy()

    if not filters_movie:
        bot.edit_message_text(
            "⚠️ Выберите хотя бы один фильтр!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=filters_keyboard()
        )
        return

    logger.info("Пользователь %s запускает поиск по фильтрам: %s", call.from_user.id, filters_movie)

    bot.edit_message_text(
        "🍿 Поиск по фильтрам... 👀",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )
    try:
        result = find_movies_by_filters(filters_movie)

        if result is None:
            bot.send_message(call.message.chat.id, "Ошибка API!", reply_markup=main_menu_keyboard())
            return
        if len(result) == 0:
            bot.send_message(call.message.chat.id, "Ничего не найдено!", reply_markup=main_menu_keyboard())
            return
        # Успешный поиск
        bot.set_state(call.from_user.id, Pagination.viewing, call.message.chat.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["films_list"] = result
            data["current_page"] = 1
            data["items_on_page"] = 5

        bot.send_message(
            call.message.chat.id,
            f"Найдено фильмов: {len(result)}",
            reply_markup=list_films_keyboard(result, page=1, items_on_page=5)
        )

    except Exception as e:
        logger.exception("Ошибка при поиске по фильтрам")
        bot.send_message(
            call.message.chat.id,
            "❌ Произошла ошибка при поиске.",
            reply_markup=main_menu_keyboard()
        )

# ====================== РЕГИСТРАЦИЯ ======================

def register_filters_handlers():
    """Регистрация всех обработчиков фильтров"""
    logger.info("Обработчики фильтров (filters.py) успешно зарегистрированы")




















