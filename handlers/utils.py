"""Заглушка для handlers/utils — основные утилиты находятся в корневом utils.py"""

import logging

logger = logging.getLogger(__name__)


def register_utils():
    """Регистрация модуля утилит заглушка"""
    logger.info("handlers/utils.py загружен (заглушка)")