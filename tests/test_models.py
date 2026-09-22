# tests/test_models.py
from models import create_user, create_poll


def test_create_user():
    """Проверяем, что пользователь создаётся с правильным ID."""
    users = {}
    user_id = create_user(users, "Алиса")

    assert user_id == 1
    assert len(users) == 1
    assert users[1]["username"] == "Алиса"


def test_create_second_user():
    """Второй пользователь должен получить ID = 2."""
    users = {}
    create_user(users, "Алиса")
    user_id = create_user(users, "Боб")

    assert user_id == 2
    assert len(users) == 2
    assert users[2]["username"] == "Боб"


def test_create_poll():
    """Проверяем создание голосования."""
    polls = {}
    poll_id = create_poll(polls, 1, "Какой язык лучше?", ["Python", "Java"])

    assert poll_id == 1
    assert len(polls) == 1
    assert polls[1]["question"] == "Какой язык лучше?"
    assert polls[1]["author_id"] == 1
    assert polls[1]["is_active"] is True


def test_poll_choices_numbering():
    """Варианты ответа должны нумероваться с 1."""
    polls = {}
    create_poll(polls, 1, "Вопрос?", ["A", "B", "C"])

    choices = polls[1]["choices"]
    assert choices[1] == "A"
    assert choices[2] == "B"
    assert choices[3] == "C"
    assert len(choices) == 3