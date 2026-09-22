from datetime import datetime


def input_int(prompt: str) -> int:
    """
    Запросить у пользователя целое число.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_string(prompt: str) -> str:
    """
    Запросить у пользователя строку.
    """
    return input(prompt).strip()