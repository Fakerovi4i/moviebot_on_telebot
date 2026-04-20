import logging
from telebot.types import Message
import json

from bot import bot
from api_requests import find_move_by_name
from keyboards import main_menu_keyboard, list_films_keyboard
from my_states import Pagination

logger = logging.getLogger(__name__)


def process_find_move_by_name(message: Message):
    """Обработка введённого названия фильма"""
    name = message.text.strip()

    if not name:
        bot.send_message(
            message.chat.id,
            "⚠️ Введите название фильма или выберете другую команду!",
            reply_markup=main_menu_keyboard()
        )
        return

    logger.info("Пользователь %s ищет фильм по названию: %s", message.from_user.id, name)

    try:
        bot.send_message(message.chat.id, "🔍 Ищу фильмы...")
        result = find_move_by_name(name)
        if result is None:
            bot.send_message(
                message.chat.id,
                'Произошла ошибка обращения к сайту!\nПопробуйте позже.',
                reply_markup=main_menu_keyboard())
            logger.error("API вернул None при поиске по названию: %s", name)
            return

        if len(result) == 0:
            bot.send_message(
                message.chat.id, 'Ничего не найдено!', reply_markup=main_menu_keyboard()
            )
            logger.info("По запросу '%s' ничего не найдено", name)
            return

        # Успешный поиск
        result = [film for film in result if isinstance(film, dict) and "id" in film]
        logger.info("Найдено %d фильмов по запросу '%s'", len(result), name)
        bot.set_state(message.from_user.id, Pagination.viewing, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["films_list"] = result
            data["current_page"] = 1
            data["items_on_page"] = 5
        bot.send_message(
            message.chat.id,
            f"Найдено фильмов: {len(result)}",
            reply_markup=list_films_keyboard(result, page=1, items_on_page=5))

    except Exception as e:
        logger.exception("Ошибка при поиске '%s'", name)
        bot.send_message(
            message.chat.id,
            '❌ Ошибка при получении данных о фильме!',
            reply_markup=main_menu_keyboard())


# ====================== MESSAGE HANDLERS ======================

@bot.message_handler(func=lambda message: message.text in ['/search', '🔍Поиск по названию'])
def find_move(message: Message):
    """Запуск команды поиска по названию"""
    logger.info("Пользователь %s вызвал поиск по названию", message.from_user.id)

    try:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(
            message.chat.id,
            "Введите название фильма для поиска:\n",
            reply_markup=None
        )
    except Exception as e:
        logger.exception("Ошибка в find_move handler")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка. Попробуйте позже.",
            reply_markup=main_menu_keyboard()
        )


@bot.message_handler(func=lambda message: True)
def handle_text(message: Message):
    """
    Универсальный обработчик текста.
    Срабатывает, если сообщение не попало в другие обработчики.
    """

    state = bot.get_state(message.from_user.id, message.chat.id)
    logger.debug("Получено текстовое сообщение. Текущее состояние: %s", state)

    #Если нет состояния или в Pagination.viewing то ищем по названию
    if state is None or state == Pagination.viewing.name:
        bot.delete_state(message.from_user.id, message.chat.id)
        process_find_move_by_name(message)
    # Если в каком-то другом состоянии — игнорируем или возвращаем в меню
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ Неизвестная команда возврат в меню 👇",
            reply_markup=main_menu_keyboard()
        )



def register_search_handlers():
    """Регистрация обработчиков модуля search"""
    logger.info("Обработчики поиска (search.py) успешно зарегистрированы")






