from project_Oscar.db.queries import (
    SEARCH_BY_KEYWORD,
    SEARCH_BY_GENRE_YEAR_BASE,
    CREATE_SEARCH_LOG_TABLE,
    INSERT_SEARCH_LOG,
    POPULAR_SEARCHES,
    GET_ALL_GENRES,
    GET_MIN_YEAR,
    GET_MAX_YEAR
)
from project_Oscar.db.connector import get_connection, get_log_connection
from project_Oscar.logic.logger import log_error
from typing import List, Tuple


def search_by_keyword(keyword: str) -> List[Tuple[int, str, int]]:
    """
    Выполняет поиск фильмов по ключевому слову в названии.

    :param keyword: Строка для поиска
    :return: Список найденных фильмов (film_id, title, release_year)
    """
    results = []
    like_pattern = f"%{keyword}%"
    conn = get_connection()
    if conn is None:
        return results
    try:
        cursor = conn.cursor()
        cursor.execute(SEARCH_BY_KEYWORD, (like_pattern,))
        results = cursor.fetchall()
        cursor.close()
    except Exception as e:
        log_error("search_by_keyword", e)
        print(f"Ошибка при выполнении запроса поиска: {e}")
    finally:
        conn.close()
    log_search("keyword", keyword)
    return results


def search_by_genre_and_year(genre: str | None, year: int | None) -> List[Tuple[int, str]]:
    """
    Выполняет поиск фильмов по жанру и/или году выпуска.
    Если жанр или год равен None, фильтрация по нему не применяется.
    """
    results = []
    conn = get_connection()
    if conn is None:
        return results

    try:
        cursor = conn.cursor()

        query = SEARCH_BY_GENRE_YEAR_BASE  # Базовый запрос из queries.py
        conditions = []
        params = []

        if genre is not None:
            conditions.append("c.name = %s")
            params.append(genre)
        if year is not None:
            conditions.append("f.release_year = %s")
            params.append(year)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " LIMIT 20;"

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        cursor.close()

    except Exception as e:
        log_error("search_by_genre_and_year", e)
        print(f"Ошибка при выполнении поиска по жанру и году: {e}")
    finally:
        conn.close()

    # Для логирования
    genre_text = genre if genre is not None else "any_genre"
    year_text = str(year) if year is not None else "any_year"
    log_search("genre_year", f"{genre_text}:{year_text}")

    return results


def log_search(search_type: str, query_text: str) -> None:
    """
    Логирует поисковый запрос в таблицу search_log с подсчётом количества и временем последнего использования.

    :param search_type: Тип запроса (например, 'keyword', 'genre_year')
    :param query_text: Содержимое запроса (что именно ввёл пользователь)
    """
    conn = get_log_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_SEARCH_LOG_TABLE)
        cursor.execute(INSERT_SEARCH_LOG, (search_type, query_text))
        conn.commit()
        cursor.close()
    except Exception as e:
        log_error("log_search", e)
        print(f"Ошибка при логировании запроса: {e}")
    finally:
        conn.close()


# def get_popular_searches(limit: int = 10) -> List[Tuple[str, int]]:
#     """
#     Возвращает список самых популярных поисковых запросов.
#
#     :param limit: Количество запросов
#     :return: Список кортежей (запрос, количество)
#     """
#     conn = get_log_connection()
#     if conn is None:
#         return []
#     try:
#         cursor = conn.cursor()
#         cursor.execute(POPULAR_SEARCHES, (limit,))
#         results = cursor.fetchall()
#         cursor.close()
#         return results
#     except Exception as e:
#         log_error("get_popular_searches", e)
#         print(f"Ошибка при получении популярных запросов: {e}")
#         return []
#     finally:
#         conn.close()


def get_all_genres() -> List[str]:
    """
    Возвращает список всех уникальных жанров из базы, отсортированных по алфавиту.
    """
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(GET_ALL_GENRES)
        genres = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return genres
    except Exception as e:
        log_error("get_all_genres", e)
        return []
    finally:
        conn.close()


def get_year_range() -> Tuple[int, int] | None:
    """
    Возвращает минимальный и максимальный год выпуска фильмов из базы.

    :return: Кортеж (min_year, max_year) или None при ошибке
    """
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(GET_MIN_YEAR)
        min_year = cursor.fetchone()[0]
        cursor.execute(GET_MAX_YEAR)
        max_year = cursor.fetchone()[0]
        cursor.close()
        return min_year, max_year
    except Exception as e:
        log_error("get_year_range", e)
        return None
    finally:
        conn.close()

