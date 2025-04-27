import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()


def get_connection(database: str = "sakila") -> mysql.connector.connection_cext.CMySQLConnection | None:
    """
    Устанавливает соединение с базой данных Sakila.

    :param database: Название базы данных (по умолчанию 'sakila')
    :return: Объект соединения или None при ошибке
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host_read"),
            user=os.getenv("user_read"),
            password=os.getenv("password_read"),
            database=database
        )
        return connection
    except Error as e:
        print(f"[Ошибка подключения к sakila] {e}")
        return None


def get_log_connection(database: str = "group_111124_fp_GolubenkoA") -> mysql.connector.connection_cext.CMySQLConnection | None:
    """
    Устанавливает соединение с базой данных логов.

    :param database: Название базы данных логов (по умолчанию 'group_111124_fp_GolubenkoA')
    :return: Объект соединения или None при ошибке
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host_write"),
            user=os.getenv("user_write"),
            password=os.getenv("password_write"),
            database=database
        )
        return connection
    except Error as e:
        print(f"[Ошибка подключения к лог-базе] {e}")
        return None
