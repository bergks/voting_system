import json
from typing import Dict, List


def load_data(filename: str) -> Dict | List:
    """
    Загрузить данные из JSON-файла.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Возвращаем пустую структуру в зависимости от ожидаемого типа
        if 'users' in filename or 'polls' in filename:
            return {}
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} содержит некорректный JSON.")
        return {} if 'users' in filename or 'polls' in filename else []


def save_data(filename: str, data: Dict | List) -> None:
    """
    Сохранить данные в JSON-файл.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)