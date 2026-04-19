"""
Общие обработчики и регистрация всех хендлеров.
"""

import logging
from telebot.types import CallbackQuery, Message

from bot import bot
from keyboards import main_menu_keyboard, list_films_keyboard, filters_keyboard
from my_states import ChoiceFilters, Pagination

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    """Обработчик команды start"""
    try:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Используй /help для списка команд 🛟\n\n"
            "Введи название фильма для поиска 🔎\n\n"
            "Или выбери одну из команд ниже 👇",
            reply_markup=main_menu_keyboard()
        )
        logger.info("Пользователь %s начал работу с ботом", message.from_user.id)
    except Exception:
        logger.exception("Ошибка в start_message")


@bot.message_handler(commands=['help'])
def help_message(message: Message):
    """Обработчик команды help"""
    try:
        help_text = """
        📋 <b>Доступные команды:</b>
        
        • /start - Перезапустить бота 
        • /search - Поиск фильма по названию
        • /filters - Поиск по фильтрам
        • /top - Топ 100 фильмов
        • /history - История поиска
        
        Или введи название фильма — бот начнёт поиск.
        """
        bot.send_message(message.chat.id, help_text, parse_mode="HTML")
        logger.info("Пользователь %s запросил помощь", message.from_user.id)
    except Exception:
        logger.exception("Ошибка в help_message")


@bot.callback_query_handler(func=lambda call: call.data in ["back_to_menu", "filters_exit"], state=[Pagination.viewing, ChoiceFilters.waiting_filters])
def back_to_menu_callback(call: CallbackQuery):
    """Возврат в главное меню"""
    try:
        bot.answer_callback_query(call.id)
        bot.delete_state(call.from_user.id, call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(
            call.message.chat.id,
            "Главное меню 👇",
            reply_markup=main_menu_keyboard()
        )
        logger.info("Пользователь %s вернулся в главное меню", call.from_user.id)
    except Exception:
        logger.exception("Ошибка в back_to_menu_callback")


@bot.callback_query_handler(func=lambda call: call.data == "back_to_list")
def callback_back_to_list(call: CallbackQuery):
    """Возврат к списку фильмов"""
    try:
        bot.answer_callback_query(call.id)
        bot.set_state(call.from_user.id, Pagination.viewing, call.message.chat.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            films_list = data.get('films_list', [])

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "Список фильмов:",
            reply_markup=list_films_keyboard(films_list)
        )
    except Exception:
        logger.exception("Ошибка в callback_back_to_list")


@bot.callback_query_handler(func=lambda call: call.data == "back_to_filters", state=ChoiceFilters.waiting_filters)
def callback_back_to_filters(call: CallbackQuery):
    """Возврат к меню фильтров"""
    try:
        bot.answer_callback_query(call.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            selected_filters = dict(data)

        bot.edit_message_text(
            "Выберите фильтры:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=filters_keyboard(selected_filters=selected_filters)
        )
    except Exception:
        logger.exception("Ошибка в callback_back_to_filters")


def register_handlers():
    """Регистрации всех обработчиков"""
    logger.info("Начинается регистрация обработчиков...")

    # Импорт модулей вызывает регистрацию декораторов
    from .filters import register_filters_handlers
    from .common_callbacks import register_common_callbacks
    from .top import register_top_handlers
    from .history import register_history_handlers
    from .search import register_search_handlers
    from .utils import register_utils




    # Вызовы функций — только для логирования
    register_filters_handlers()
    register_common_callbacks()
    register_top_handlers()
    register_history_handlers()
    register_search_handlers()
    register_utils()

    logger.info("Регистрация всех обработчиков завершена.")












