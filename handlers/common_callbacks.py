"""
Общие Колбэки:
- Открытие карточки фильма
- Пагинация
- Навигационные кнопки
"""

import logging
import requests
from io import BytesIO
from telebot.types import CallbackQuery

from bot import bot
from api_requests import get_movie_by_id
from keyboards import (
    list_films_keyboard,
    back_to_list_main_menu_button,
    main_menu_keyboard
)
from database.db_util import add_movie_to_history
from my_states import Pagination
from utils import create_google_link, info_about_move


logger = logging.getLogger(__name__)


@bot.callback_query_handler(func=lambda call: call.data.startswith("film_"))
def callback_film_id_handler(call: CallbackQuery):
    """Обработчик нажатия на кнопку фильма"""
    bot.answer_callback_query(call.id)

    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        movie_id = int(call.data.split("_")[1])
        logger.info("Пользователь %s открыл фильм ID: %d", call.from_user.id, movie_id)

        movie_data = get_movie_by_id(movie_id)
        if not movie_data:
            bot.send_message(call.message.chat.id, "❌ Не удалось загрузить информацию о фильме.")
            return

        name, poster, kp_rate, year, countries, url, description = info_about_move(movie_data)

        info = f"🎬 {name}\n{countries} | {year} | Рейтинг: {kp_rate}\n"

        url_google = create_google_link(name)

        if url is None:
            urls_for_watch = f"\n[Искать в Google]({url_google})\n\n"
        else:
            urls_for_watch = f"\n🍿 [Смотреть]({url})\n\n[Искать в Google]({url_google})\n\n"

        if description is None:
            description = "Описание:\nНет описания."
        else:
            description = f"Описание:\n{description}"

        add_movie_to_history(call.from_user.id, movie_id, movie_data)

        try:
            response = requests.get(poster, timeout=15)
            response.raise_for_status()  # проверяем, что запрос успешен
            photo_file = BytesIO(response.content)

            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo_file,  # ← отправляем байты, а не URL
                caption=info + urls_for_watch + description,
                parse_mode="Markdown",
                reply_markup=back_to_list_main_menu_button()
            )
        except requests.exceptions.RequestException:
            logger.warning("Не удалось загрузить постер для фильма %d", movie_id)
            # Если не удалось скачать — отправляем хотя бы текст
            bot.send_message(
                call.message.chat.id,
                info + urls_for_watch + description,
                parse_mode="Markdown",
                reply_markup=back_to_list_main_menu_button()
            )

    except Exception:
        logger.exception("Ошибка в callback_film_id_handler для фильма %s", call.data)
        bot.send_message(call.message.chat.id, "❌ Произошла ошибка при открытии фильма.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("page_"), state=Pagination.viewing)
def pagination_callback(call: CallbackQuery):
    """Обработчик переключения страниц списка ПАГИНАЦИЯ"""
    bot.answer_callback_query(call.id)
    page = int(call.data.split("_")[1])

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        films = data.get("films_list", [])
        items_on_page = data.get("items_on_page", 5)

    if not films:
        bot.send_message(call.message.chat.id, "Список фильмов не найден!", reply_markup=main_menu_keyboard())
        bot.delete_state(call.from_user.id, call.message.chat.id)
        return

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["current_page"] = page

    total_pages = (len(films) + items_on_page - 1) // items_on_page


    bot.edit_message_text(
        f"Найдено фильмов: {len(films)}\nСтраница {page} из {total_pages}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=list_films_keyboard(films, page=page, items_on_page=items_on_page)
    )



def register_common_callbacks():
    """Регистрация общих Колбэков"""
    logger.info("Общие callback-обработчики (common_callbacks.py) успешно зарегистрированы")











