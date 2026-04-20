"""Модуль утилит для обработки данных и создания ссылок"""


import logging
import urllib.parse
from typing import Any, Dict

logger = logging.getLogger(__name__)

def info_about_move(data: Dict[str, Any]):
    """
    Извлекает основную информацию о фильме из данных API.
    Возвращает: (name, poster, kp_rate, year, countries, url, description)
    """
    try:
        print(data)
        name = data.get("name", None)
        if name is None:
            name = data.get("names", [])
            if name and isinstance(name, list):
                name = name[0].get("name", None)
        if name is None:
            name = data.get("alternativeName", "Без названия")

        poster = data.get("poster", {}).get("previewUrl", None)
        #Если нет постера то заглушка
        if poster is None:
            poster = "https://dummyimage.com/300x450/2c3e50/ffffff.png&text=No+Poster"

        rating = data.get("rating", {})
        if rating is None:
            rating = {}

        kp_rate = rating.get("kp", "-")
        if kp_rate is None:
            kp_rate = "-"

        year = data.get("year", "-")

        countries = data.get("countries", [{}])
        country_name = countries[0].get("name", "-") if countries else "-"

        url = None
        if "watchability" in data and data["watchability"].get("items"):
            url = data["watchability"]["items"][0].get("url", None)

        description = data.get("description", None)

        return name, poster, kp_rate, year, country_name, url, description

    except Exception:
        logger.exception("Ошибка при обработке данных фильма")
        # Возвращаем безопасные значения по умолчанию
        return "Ошибка загрузки", "https://dummyimage.com/300x450/2c3e50/ffffff.png&text=Error", "-", "-", "-", None, "Нет описания"

def create_google_link(name: str) -> str:
    """Создаёт ссылку на Google поиск фильма"""
    try:
        encoded_query = urllib.parse.quote(f"{name} смотреть онлайн")
        return f"https://www.google.com/search?q={encoded_query}"
    except Exception:
        logger.warning("Не удалось создать Google ссылку для фильма: %s", name)
        return "https://www.google.com/search?q=смотреть+онлайн"


def register_utils():
    """Регистрация утилит"""
    logger.info("Утилиты utils.py загружены")