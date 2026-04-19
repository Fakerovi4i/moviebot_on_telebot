import requests
from typing import Dict, Any
import logging

from config import API_HOST, SITE_API_KEY, API_TIMEOUT


logger = logging.getLogger(__name__)

headers = {"X-API-KEY": SITE_API_KEY}


def get_movie_by_id(movie_id: int):
    """Получение фильма по ID"""
    try:
        url = f"{API_HOST}/movie/{movie_id}"
        response = requests.get(
            url,
            headers=headers,
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        logger.warning(f"API вернул код %s", response.status_code)
        return None
    except requests.Timeout:
        logger.warning("Превышено время ожидания от API")
        return None
    except requests.ConnectionError:
        logger.warning("Ошибка подключения к API")
        return None
    except Exception as e:
        logger.error("Неожиданная ошибка от API: %s", e)
        return None


def find_move_by_name(move_name: str, page=1, limit=50):
    """Поиск по названию"""
    try:
        url = f"{API_HOST}/movie/search"
        params = {"query": move_name, "page": page, "limit": limit}
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=API_TIMEOUT

        )
        if response.status_code == 200:
            return response.json().get("docs", [])

        logger.warning(f"API вернул код %s", response.status_code)
        return None

    except requests.Timeout:
        logger.warning("Превышено время ожидания от API")
        return None

    except requests.ConnectionError:
        logger.warning("Ошибка подключения к API")
        return None

    except Exception as e:
        logger.error("Неожиданная ошибка от API: %s", e)
        return None


def find_movies_by_filters(filters: Dict[str, str], page=1, limit=50):
    """Поиск фильмов по фильтрам"""

    try:
        url = f"{API_HOST}/movie"
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }

        if 'rating' in filters:
            params["rating.kp"] = f"{filters['rating']}-10"
            params["sortField"] = "rating.kp"
            params["sortType"] = "-1"
        if 'genre' in filters and filters['genre']:
            params["genres.name"] = ",".join(filters['genre'])
        if 'year_with' in filters or 'year_to' in filters:
            params["year"] = f"{filters['year_with']}-{filters['year_to']}"
        if 'country' in filters and filters['country']:
            params["countries.name"] = ",".join(filters['country'])

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json().get("docs", [])

        logger.warning(f"API вернул код %s", response.status_code)
        return None

    except requests.Timeout:
        logger.warning("Превышено время ожидания от API")
        return None

    except requests.ConnectionError:
        logger.warning("Ошибка подключения к API")
        return None

    except Exception as e:
        logger.error("Неожиданная ошибка от API: %s", e)
        return None



def find_top_100(page=1, limit=100):
    try:
        url = f"{API_HOST}/movie"
        params = {
            "page": page,
            "limit": limit,
            "sortField": "votes.kp",
            "sortType": "-1",
            "lists": "top250"}

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json().get("docs", [])

        logger.warning("API вернул код %s", response.status_code)
        return None

    except requests.Timeout:
        logger.warning("Превышено время ожидания от API")
        return None

    except requests.ConnectionError:
        logger.warning("Ошибка подключения к API")
        return None

    except Exception as e:
        logger.error("Неожиданная ошибка от API: %s", e)
        return None



if __name__ == "__main__":
    logger.info("Тестирование API")
    result = find_movies_by_filters({"rating": "6"})
    if result is None:
        print("❌ Произошла ошибка при обращении к API")
    elif len(result) == 0:
        print("😔 Фильм не найден")
    else:
        print(f"✅ Найдено фильмов: {len(result)}")
        print(f"Первый результат: {result[0].get('name', 'Без названия')}")
        print(result)

