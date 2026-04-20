"""
Главный файл запуска Telegram-бота.
"""
import logging
from logging_config import setup_logging
import time
from telebot.apihelper import ApiTelegramException

from bot import bot
from database.db_connection import init_db
from handlers.base import register_handlers




def main():
    setup_logging(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("🤖 Бот запущен...")

    init_db()
    register_handlers()

    while True:
        try:
            logger.info("🤖 Бот начал работу...")
            bot.infinity_polling(
                skip_pending=True,
                timeout=60,
                long_polling_timeout=60
            )
        except ApiTelegramException as e:
            if e.result_json.get('error_code') == 409:
                logger.warning("Обнаружен конфликт экземпляров (409). Перезапуск через 5 секунд...")
                time.sleep(5)
                continue
            else:
                logger.critical(f"Неизвестная ошибка Telegram API: {e}", exc_info=True)
                break
        except Exception as e:
            logger.critical(f"Критическая ошибка: {e}", exc_info=True)
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.critical("Критическая ошибка при запуске бота", exc_info=True)
