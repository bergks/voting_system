# models.py
from datetime import datetime


def create_user(users: dict, username: str) -> int:
    """Создать нового пользователя.

    Возвращает ID нового пользователя.
    """
    user_id = 1
    if users:
        user_id = max(users.keys()) + 1

    users[user_id] = {
        "id": user_id,
        "username": username,
        "created_at": datetime.now().isoformat()
    }
    return user_id


def create_poll(polls: dict, author_id: int, question: str, choices: list) -> int:
    """Создать новое голосование.

    Возвращает ID нового голосования.
    """
    poll_id = 1
    if polls:
        poll_id = max(polls.keys()) + 1

    # Собираем варианты ответа в словарь {1: "текст", 2: "текст"}
    choices_dict = {}
    number = 1
    for text in choices:
        choices_dict[number] = text
        number += 1

    polls[poll_id] = {
        "id": poll_id,
        "author_id": author_id,
        "question": question,
        "choices": choices_dict,
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    return poll_id


def get_poll_results(polls: dict, votes: list, poll_id: int) -> dict | None:
    """Посчитать результаты голосования.

    Возвращает словарь {вариант: количество} или None, если опроса нет.
    """
    if poll_id not in polls:
        return None

    poll = polls[poll_id]

    # Сначала обнуляем счётчики для всех вариантов
    results = {}
    for text in poll["choices"].values():
        results[text] = 0

    # Пробегаем по всем голосам и увеличиваем счётчик
    for vote in votes:
        if vote["poll_id"] == poll_id:
            choice_id = vote["choice_id"]
            if choice_id in poll["choices"]:
                choice_text = poll["choices"][choice_id]
                results[choice_text] += 1

    return results


def cast_vote(votes: list, polls: dict, user_id: int, poll_id: int, choice_id: int) -> bool:
    """Отдать голос за вариант.

    Возвращает True, если голос принят, иначе False.
    """
    if poll_id not in polls:
        return False

    poll = polls[poll_id]

    if not poll["is_active"]:
        return False

    if choice_id not in poll["choices"]:
        return False

    # Проверяем, не голосовал ли уже этот пользователь
    for vote in votes:
        if vote["user_id"] == user_id and vote["poll_id"] == poll_id:
            return False

    votes.append({
        "user_id": user_id,
        "poll_id": poll_id,
        "choice_id": choice_id,
        "voted_at": datetime.now().isoformat()
    })
    return True
