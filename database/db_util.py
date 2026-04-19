import json
from .db_connection import get_connection

def add_movie_to_history(user_id: int, movie_id: int, movie_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    movie_json = json.dumps(movie_data, ensure_ascii=False)

    (cursor.execute
        ("""UPDATE history SET search_date=CURRENT_TIMESTAMP,
        movie_data=? WHERE user_id=? AND movie_id=?""",
        (movie_json, user_id, movie_id)))

    if cursor.rowcount == 0:
        cursor.execute(
            """INSERT INTO history 
            (user_id, movie_id, movie_data) VALUES (?, ?, ?)""",
            (user_id, movie_id, movie_json)
        )
        cursor.execute(
            """DELETE FROM history WHERE user_id=? AND id NOT IN (
            SELECT id FROM history WHERE user_id=?
             ORDER BY search_date DESC LIMIT 10)""",
            (user_id, user_id)
        )

    conn.commit()
    conn.close()

def get_user_history(user_id: int) -> list:
    """Возвращает историю просмотров пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT movie_data FROM history 
        WHERE user_id=? ORDER BY search_date DESC LIMIT 10""",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in rows]



