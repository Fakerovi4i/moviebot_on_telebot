"""
Главный файл запуска Telegram-бота.
"""
import logging
from logging_config import setup_logging

from bot import bot
from database.db_connection import init_db
from handlers.base import register_handlers

import os
import threading
from flask import Flask


# --- Создаем простое Flask-приложение для Health Check ---
flask_app = Flask(__name__)

@flask_app.route('/')
@flask_app.route('/health')
def health_check():
    return "OK", 200

def run_web_server():
    """Запускает Flask-сервер, который будет слушать порт, назначенный Render."""
    port = int(os.environ.get('PORT', 5000))
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


def main():
    print(">>> Бот начал загрузку...", flush=True)
    setup_logging(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("🤖 Бот запущен...")

    init_db()
    register_handlers()

    # Запускаем веб-сервер для Health Check в отдельном потоке
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info("🌐 Веб-сервер для Health Check запущен.")

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
        # Сделано для отладки
        print(f"FATAL ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()