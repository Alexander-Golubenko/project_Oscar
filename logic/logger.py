import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "errors.log"),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

def log_error(context: str, error: Exception) -> None:
    """
    Записывает сообщение об ошибке в файл логов.

    :param context: Название функции или области, где произошла ошибка
    :param error: Исключение
    """
    logging.error(f"{context}: {str(error)}")