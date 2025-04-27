from project_Oscar.logic.details import get_film_details
from project_Oscar.logic.search import get_all_genres, get_year_range
from typing import List, Tuple


def show_menu() -> str:
    """
    Отображает главное меню и возвращает выбор пользователя.
    """
    print("\n--- Меню ---")
    print("1. Поиск по ключевому слову")
    print("2. Поиск по жанру и году")
    print("3. Показать популярные запросы")
    print("0. Завершить программу\n")
    return input("Выберите один из вариантов ( 1 / 2 / 3 / 0 ): ").strip()


def ask_keyword() -> str:
    """
    Запрашивает у пользователя ключевое слово для поиска.
    """
    return input("Введите ключевое слово для поиска фильмов: ").strip()


def ask_genre_and_year() -> Tuple[str | None, int | None] | None:
    """
    Запрашивает у пользователя жанр (или Enter для любого) и год выпуска (или Enter для любого).
    """
    genres = get_all_genres()
    if not genres:
        print("Не удалось получить список жанров.")
        return None

    # выбор жанра
    print("\nДоступные жанры:")
    for i, genre in enumerate(genres, start=1):
        print(f"{i}. {genre}")

    selected_genre = None
    while True:
        genre_input = input("Выберите номер жанра или нажмите Enter для любого жанра: ").strip()
        if genre_input == "":
            selected_genre = None
            break
        if genre_input.isdigit():
            genre_choice = int(genre_input)
            if 1 <= genre_choice <= len(genres):
                selected_genre = genres[genre_choice - 1]
                break
            else:
                print("Неверный номер жанра. Попробуйте ещё раз.")
        else:
            print("Ошибка ввода. Введите номер жанра или Enter для пропуска.")

    # выбор года
    year_range = get_year_range(selected_genre)
    if not year_range:
        print("Не удалось получить диапазон лет.")
        return None

    min_year, max_year = year_range
    print(f"Допустимый диапазон лет: {min_year} – {max_year}")

    selected_year = None
    while True:
        year_input = input("Введите год выпуска или нажмите Enter для любого года: ").strip()
        if year_input == "":
            selected_year = None
            break
        if year_input.isdigit():
            year = int(year_input)
            if min_year <= year <= max_year:
                selected_year = year
                break
            else:
                print("Год вне допустимого диапазона. Попробуйте ещё раз.")
        else:
            print("Ошибка ввода. Введите корректный год или Enter для пропуска.")

    return selected_genre, selected_year


def show_search_results(results: List[Tuple], show_year: bool = True) -> int | None:
    """
    Отображает список фильмов и предлагает выбрать один для просмотра деталей.
    """
    if not results:
        print("\nПо вашему запросу ничего не найдено.")
        return None

    while True:
        print("\nНайденные фильмы:")
        for i, item in enumerate(results, start=1):
            title = f"{item[1]} ({item[2]})" if show_year and len(item) > 2 else item[1]
            print(f"{i}. {title}")

        sub_choice = input("Введите номер фильма для подробностей или нажмите Enter для пропуска: ").strip()

        if sub_choice == "":
            return None  # User решил пропустить

        if sub_choice.isdigit():
            index = int(sub_choice) - 1
            if 0 <= index < len(results):
                return results[index][0]
            else:
                print("Неверный номер фильма. Попробуйте ещё раз.")
        else:
            print("Ошибка ввода. Введите номер фильма или просто Enter.")

def ask_continue() -> bool:
    """
    Спрашивает пользователя, хочет ли он продолжить работу с приложением.
    """
    while True:
        again = input("\nСделать ещё один запрос? (Y/N): ").strip().lower()
        if again in ("y", "yes"):
            return True
        elif again in ("n", "no"):
            return False
        else:
            print("Пожалуйста, введите Y или N.")


def show_popular_queries(queries: List[Tuple[str, int]]) -> None:
    """
    Отображает список популярных запросов с частотами.
    """
    if queries:
        print("\nПопулярные поисковые запросы:")
        for i, (term, freq) in enumerate(queries, start=1):
            print(f"{i}. {term} — {freq} раз(а)")
    else:
        print("Нет записей поисковых запросов.")

