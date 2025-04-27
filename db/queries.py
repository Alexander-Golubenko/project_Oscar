SEARCH_BY_KEYWORD = """
    SELECT film_id, title, release_year
    FROM film
    WHERE title LIKE %s
    LIMIT 20;
"""


SEARCH_BY_GENRE_YEAR_BASE = """
    SELECT f.film_id, f.title
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
"""


CREATE_SEARCH_LOG_TABLE = """
    CREATE TABLE IF NOT EXISTS search_log (
        search_type VARCHAR(50),
        query_text VARCHAR(255),
        query_count INT DEFAULT 1,
        last_queried TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (search_type, query_text)
    )
"""


INSERT_SEARCH_LOG = """
    INSERT INTO search_log (search_type, query_text, query_count, last_queried)
    VALUES (%s, %s, 1, NOW())
    ON DUPLICATE KEY UPDATE
        query_count = query_count + 1,
        last_queried = NOW();
"""


POPULAR_SEARCHES = """
    SELECT query_text, query_count
    FROM search_log
    ORDER BY query_count DESC
    LIMIT %s;
"""


GET_ALL_GENRES = """
    SELECT DISTINCT name
    FROM category
    ORDER BY name;
"""


GET_MIN_YEAR = """
    SELECT MIN(release_year) FROM film;
"""


GET_MAX_YEAR = """
    SELECT MAX(release_year) FROM film;
"""


GET_MIN_YEAR_BY_GENRE = """
    SELECT MIN(f.release_year)
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s;
"""


GET_MAX_YEAR_BY_GENRE = """
    SELECT MAX(f.release_year)
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s;
"""


GET_FILM_DETAILS = """
        SELECT f.title, \
               f.description, \
               f.release_year, \
               f.length, \
               l.name AS language,
           GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors,
           GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories
        FROM film f
            JOIN language l \
        ON f.language_id = l.language_id
            JOIN film_actor fa ON f.film_id = fa.film_id
            JOIN actor a ON fa.actor_id = a.actor_id
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
        WHERE f.film_id = %s
        GROUP BY f.film_id; \
        """