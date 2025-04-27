from project_Oscar.db.connector import get_connection
from project_Oscar.logic.logger import log_error
from project_Oscar.db.queries import GET_FILM_DETAILS
from tabulate import tabulate
import textwrap


def get_film_details(film_id: int) -> None:
    """
    Выводит карточку фильма в вертикальном виде с переносом длинных строк.

    :param film_id: ID фильма для отображения
    """
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(GET_FILM_DETAILS, (film_id,))
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
