"""
Обработчики команды /top — Топ 100 фильмов.
"""
import logging
from telebot.types import Message

from bot import bot
from api_requests import find_top_100
from keyboards import list_films_keyboard, main_menu_keyboard
from my_states import Pagination

logger = logging.getLogger(__name__)


@bot.message_handler(func=lambda message: message.text in ['/top', '⭐Топ 100'])
def top_100(message: Message):
    """Топ 100 фильмов"""
    logger.info("Пользователь %s запросил Топ 100 фильмов", message.from_user.id)

    msg = bot.send_message(
        message.chat.id,
        "🍿 Ищу Топ 100 фильмов 👀...",
        reply_markup=None
    )

    try:
        result = find_top_100()
        if result is None:
            bot.edit_message_text(
                "❌ Ошибка при обращении к API. Попробуйте позже.",
                message.chat.id,
                msg.message_id,
                reply_markup=main_menu_keyboard()
            )
            return

        if len(result) == 0:
            bot.edit_message_text(
                "😔 Ничего не найдено.",
                message.chat.id,
                msg.message_id,
                reply_markup=main_menu_keyboard()
            )
            return

        #Успешно найдены фильмы
        bot.set_state(message.from_user.id, Pagination.viewing, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["films_list"] = result
            data["current_page"] = 1
            data["items_on_page"] = 5

        bot.edit_message_text(
            "🍿 Топ 100 фильмов 👇",
            message.chat.id,
            msg.message_id,
            reply_markup=list_films_keyboard(result)
        )

        logger.info("Топ 100 успешно загружен (%d фильмов)", len(result))

    except Exception as e:
        logger.exception("Ошибка при получении Топ 100")
        bot.edit_message_text(
            "❌ Произошла ошибка при загрузке топа.",
            message.chat.id,
            msg.message_id,
            reply_markup=main_menu_keyboard()
        )

def register_top_handlers():
    """Регистрация обработчиков топа"""
    logger.info("Обработчики Топ 100 (top.py) успешно зарегистрированы")

