import logging
import sys
from pathlib import Path


def setup_logging(level=logging.INFO):
    """Настройка логирования для всего проекта"""

    # Создаём папку для логов, если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),  # вывод в консоль
            logging.FileHandler(log_dir/"bot.log", encoding='utf-8', mode='w')
        ]
    )

    # Убираем слишком шумные логи от библиотек
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("telebot").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


