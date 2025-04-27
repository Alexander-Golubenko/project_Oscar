from project_Oscar.db.connector import get_connection
from project_Oscar.logic.logger import log_error
from tabulate import tabulate
import textwrap


def get_film_details(film_id: int) -> None:
    """
    Выводит карточку фильма в вертикальном виде с переносом длинных строк.

    :param film_id: ID фильма для отображения
    """
    query = """
        SELECT f.title, f.description, f.release_year, f.length, l.name AS language,
               GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors,
               GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories
        FROM film f
        JOIN language l ON f.language_id = l.language_id
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE f.film_id = %s
        GROUP BY f.film_id;
    """

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(query, (film_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            result = list(result)

            result[1] = textwrap.fill(result[1], width=80)  #"Описание"
            result[5] = textwrap.fill(result[5], width=80)  #"Актёры"
            result[6] = textwrap.fill(result[6], width=80)  # "Жанры"

            labels = [
                "Название фильма", "Описание", "Год",
                "Длительность, мин", "Язык", "Актёры", "Жанры"
            ]
            table = list(zip(labels, result))
            print("\n" + tabulate(table, tablefmt="grid"))
        else:
            print("Фильм не найден.")

    except Exception as e:
        log_error("get_film_details", e)
        print(f"Ошибка при получении карточки фильма: {e}")

    finally:
        conn.close()
