from datetime import datetime
from typing import Dict, List, Optional


def create_user(users: Dict[int, dict], username: str) -> int:
    """
    Создать нового пользователя и добавить его в словарь users.
    """
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {
        "id": user_id,
        "username": username,
        "created_at": datetime.now().isoformat()
    }
    return user_id


def create_poll(polls: Dict[int, dict], author_id: int, question: str,
                choices: List[str]) -> int:
    """
    Создать новое голосование.
    """
    poll_id = max(polls.keys(), default=0) + 1
    polls[poll_id] = {
        "id": poll_id,
        "author_id": author_id,
        "question": question,
        "choices": {i: choice for i, choice in enumerate(choices, start=1)},
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    return poll_id


def get_poll_results(polls: Dict[int, dict], votes: List[dict],
                     poll_id: int) -> Optional[Dict[str, int]]:
    """
    Подсчитать результаты голосования.
    """
    poll = polls.get(poll_id)
    if not poll:
        return None

    results = {choice_text: 0 for choice_text in poll["choices"].values()}

    for vote in votes:
        if vote["poll_id"] == poll_id:
            choice_id = vote["choice_id"]
            choice_text = poll["choices"].get(choice_id)
            if choice_text:
                results[choice_text] += 1

    return results


def cast_vote(votes: List[dict], polls: Dict[int, dict], user_id: int,
              poll_id: int, choice_id: int) -> bool:
    """
    Проголосовать за вариант.
    """
    poll = polls.get(poll_id)
    if not poll or not poll["is_active"]:
        return False

    if choice_id not in poll["choices"]:
        return False

    # Проверка, не голосовал ли уже пользователь
    for vote in votes:
        if vote["user_id"] == user_id and vote["poll_id"] == poll_id:
            return False  # Повторное голосование запрещено

    votes.append({
        "user_id": user_id,
        "poll_id": poll_id,
        "choice_id": choice_id,
        "voted_at": datetime.now().isoformat()
    })
    return True