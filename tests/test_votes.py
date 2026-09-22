# tests/test_votes.py
from models import create_poll, cast_vote, get_poll_results


def test_cast_vote():
    """Первый голос должен приниматься."""
    polls = {}
    create_poll(polls, 1, "Вопрос?", ["Да", "Нет"])
    votes = []

    result = cast_vote(votes, polls, user_id=1, poll_id=1, choice_id=1)

    assert result is True
    assert len(votes) == 1
    assert votes[0]["user_id"] == 1
    assert votes[0]["poll_id"] == 1
    assert votes[0]["choice_id"] == 1


def test_duplicate_vote_forbidden():
    """Один пользователь не может голосовать дважды в одном опросе."""
    polls = {}
    create_poll(polls, 1, "Вопрос?", ["Да", "Нет"])
    votes = []

    cast_vote(votes, polls, user_id=1, poll_id=1, choice_id=1)
    result = cast_vote(votes, polls, user_id=1, poll_id=1, choice_id=2)

    assert result is False
    assert len(votes) == 1


def test_vote_for_nonexistent_poll():
    """Нельзя голосовать в несуществующем опросе."""
    polls = {}
    votes = []

    result = cast_vote(votes, polls, user_id=1, poll_id=99, choice_id=1)

    assert result is False
    assert len(votes) == 0


def test_vote_for_invalid_choice():
    """Нельзя выбрать несуществующий вариант."""
    polls = {}
    create_poll(polls, 1, "Вопрос?", ["Да", "Нет"])
    votes = []

    result = cast_vote(votes, polls, user_id=1, poll_id=1, choice_id=99)

    assert result is False
    assert len(votes) == 0


def test_get_poll_results():
    """Проверяем правильный подсчёт голосов."""
    polls = {}
    create_poll(polls, 1, "Вопрос?", ["Да", "Нет"])
    votes = []

    cast_vote(votes, polls, user_id=1, poll_id=1, choice_id=1)
    cast_vote(votes, polls, user_id=2, poll_id=1, choice_id=1)
    cast_vote(votes, polls, user_id=3, poll_id=1, choice_id=2)

    results = get_poll_results(polls, votes, poll_id=1)

    assert results is not None
    assert results["Да"] == 2
    assert results["Нет"] == 1


def test_get_poll_results_empty():
    """Если никто не голосовал — все счётчики по нулям."""
    polls = {}
    create_poll(polls, 1, "Вопрос?", ["Да", "Нет"])
    votes = []

    results = get_poll_results(polls, votes, poll_id=1)

    assert results is not None
    assert results["Да"] == 0
    assert results["Нет"] == 0


def test_get_results_for_nonexistent_poll():
    """Для несуществующего опроса возвращается None."""
    polls = {}
    votes = []

    results = get_poll_results(polls, votes, poll_id=99)

    assert results is None