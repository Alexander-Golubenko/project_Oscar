from project_Oscar.db.connector import get_log_connection
from project_Oscar.db.queries import POPULAR_SEARCHES
from project_Oscar.logic.logger import log_error
from typing import List, Tuple


def get_popular_searches(limit: int = 10) -> List[Tuple[str, int]]:
    """
    Возвращает список самых популярных поисковых запросов.

    :param limit: Количество запросов
    :return: Список кортежей (запрос, количество)
    """
    conn = get_log_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(POPULAR_SEARCHES, (limit,))
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        log_error("get_popular_searches", e)
        print(f"Ошибка при получении популярных запросов: {e}")
        return []
    finally:
        conn.close()