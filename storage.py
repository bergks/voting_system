# storage.py
import json


def load_users(filename: str) -> dict:
    """Загрузить пользователей из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return {}


def load_polls(filename: str) -> dict:
    """Загрузить голосования из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return {}


def load_votes(filename: str) -> list:
    """Загрузить голоса из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён.")
        return []


def save_data(filename: str, data) -> None:
    """Сохранить данные в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
