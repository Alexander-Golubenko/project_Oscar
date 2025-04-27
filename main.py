from project_Oscar.logic.search import search_by_keyword, search_by_genre_and_year
from project_Oscar.logic.analytics import get_popular_searches
from project_Oscar.ui.console import (
    show_menu,
    ask_keyword,
    ask_genre_and_year,
    show_search_results,
    show_popular_queries,
    ask_continue
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
            keyword = ask_keyword()
            if not keyword:
                print("Пустой ввод. Попробуйте снова.")
                continue
            results = search_by_keyword(keyword)
            film_id = show_search_results(results)
            if film_id:
                get_film_details(film_id)


        elif choice == "2":
            genre_year = ask_genre_and_year()
            if genre_year is None:
                continue
            genre, year = genre_year
            results = search_by_genre_and_year(genre, year)
            if not results:
                print("\nПо вашему запросу ничего не найдено.")
            else:
                film_id = show_search_results(results, show_year=False)
                if film_id:
                    get_film_details(film_id)

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