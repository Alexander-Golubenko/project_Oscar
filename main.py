from project_Oscar.logic.search import search_by_keyword, search_by_genre_and_year
from project_Oscar.logic.analytics import get_popular_searches
from project_Oscar.ui.console import (
    show_menu,
    show_popular_queries,
    ask_continue,
    run_keyword_search,
    run_genre_year_search
)
from project_Oscar.logic.details import get_film_details


def main() -> None:
    """
    Основная точка входа программы. Отображает меню и обрабатывает пользовательские команды.
    """
    while True:
        choice = show_menu()

        if choice == "0":
            print("Завершение работы.")
            break
        elif choice == "1":
            run_keyword_search()
        elif choice == "2":
            run_genre_year_search()
        elif choice == "3":
            queries = get_popular_searches()
            show_popular_queries(queries)
        else:
            print("Неверный выбор. Попробуйте снова.")

        if not ask_continue():
            print("Завершение работы.")
            break


if __name__ == "__main__":
    main()