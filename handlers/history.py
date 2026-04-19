"""
Обработчики команды /history — История поиска пользователя.
"""

import logging
from telebot.types import Message

from bot import bot
from database.db_util import get_user_history
from keyboards import list_films_keyboard, main_menu_keyboard
from my_states import Pagination

logger = logging.getLogger(__name__)


@bot.message_handler(func=lambda message: message.text in ['/history', '📜История поиска'])
def history_handler(message: Message):
    """История поиска пользователя"""
    logger.info("Пользователь %s открыл историю поиска", message.from_user.id)

    history = get_user_history(message.from_user.id)

    if not history:
        bot.send_message(message.chat.id, "📭 История просмотров пуста!", reply_markup=main_menu_keyboard())
        return

    bot.set_state(message.from_user.id, Pagination.viewing, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["films_list"] = history

    bot.send_message(
        message.chat.id,
        f"📜 История просмотров:",
        reply_markup=list_films_keyboard(history, items_on_page=10)
    )

def register_history_handlers():
    """Регистрация обработчиков истории"""
    logger.info("Обработчики истории (history.py) успешно зарегистрированы")