"""
Главный файл запуска Telegram-бота.
"""
import logging
from logging_config import setup_logging

from bot import bot
from database.db_connection import init_db
from handlers.base import register_handlers


def main():
    setup_logging(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("🤖 Бот запущен...")

    init_db()
    register_handlers()

    logger.info("🤖 Бот начал работу...")

    bot.infinity_polling(
        skip_pending=True,
        timeout=60,
        long_polling_timeout=60
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.critical("Критическая ошибка при запуске бота", exc_info=True)
