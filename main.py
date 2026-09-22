# main.py
from models import create_user, create_poll, get_poll_results, cast_vote
from storage import load_users, load_polls, load_votes, save_data
from utils import input_int, input_string

USERS_FILE = "data/users.json"
POLLS_FILE = "data/polls.json"
VOTES_FILE = "data/votes.json"


def show_polls(polls):
    """Показать список всех голосований."""
    if not polls:
        print("Голосований пока нет.")
        return

    print("\n--- Список голосований ---")
    for poll_id in polls:
        poll = polls[poll_id]
        if poll["is_active"]:
            status = "активно"
        else:
            status = "завершено"
        print(f"[{poll_id}] {poll['question']} ({status})")


def show_results(polls, votes):
    """Показать результаты выбранного голосования."""
    poll_id = input_int("Введите ID голосования: ")
    results = get_poll_results(polls, votes, poll_id)

    if results is None:
        print("Голосование не найдено.")
        return

    print(f"\n--- Результаты голосования #{poll_id} ---")
    for choice in results:
        print(f"{choice}: {results[choice]} голосов")


def main():
    """Главная функция — меню программы."""
    users = load_users(USERS_FILE)
    polls = load_polls(POLLS_FILE)
    votes = load_votes(VOTES_FILE)

    current_user_id = None

    while True:
        print("\n=== Система Голосования ===")
        if current_user_id is not None:
            print(f"Вы вошли как: {users[current_user_id]['username']}")
        else:
            print("Вы не авторизованы.")
        print("1. Войти")
        print("2. Создать голосование")
        print("3. Проголосовать")
        print("4. Показать результаты")
        print("5. Показать все голосования")
        print("0. Выход")

        choice = input_int("Выберите действие: ")

        if choice == 1:
            username = input_string("Введите имя пользователя: ")

            # Ищем пользователя с таким именем
            found_id = None
            for uid in users:
                if users[uid]["username"] == username:
                    found_id = uid
                    break

            if found_id is None:
                current_user_id = create_user(users, username)
                save_data(USERS_FILE, users)
                print(f"Создан новый пользователь: {username}")
            else:
                current_user_id = found_id
                print(f"С возвращением, {username}!")

        elif choice == 2:
            if current_user_id is None:
                print("Сначала войдите в систему.")
                continue

            question = input_string("Введите вопрос голосования: ")
            choices = []

            while True:
                text = input_string("Вариант ответа (пусто — закончить): ")
                if text == "":
                    break
                choices.append(text)

            if len(choices) < 2:
                print("Нужно минимум два варианта.")
                continue

            poll_id = create_poll(polls, current_user_id, question, choices)
            save_data(POLLS_FILE, polls)
            print(f"Голосование создано! ID: {poll_id}")

        elif choice == 3:
            if current_user_id is None:
                print("Сначала войдите в систему.")
                continue

            show_polls(polls)

            if not polls:
                continue

            poll_id = input_int("Введите ID голосования: ")

            if poll_id not in polls:
                print("Голосование не найдено.")
                continue

            poll = polls[poll_id]
            print("Варианты ответа:")
            for cid in poll["choices"]:
                print(f"{cid}. {poll['choices'][cid]}")

            choice_id = input_int("Введите номер варианта: ")

            if cast_vote(votes, polls, current_user_id, poll_id, choice_id):
                save_data(VOTES_FILE, votes)
                print("Голос принят!")
            else:
                print("Не удалось проголосовать (уже голосовали или неверный вариант).")

        elif choice == 4:
            show_results(polls, votes)

        elif choice == 5:
            show_polls(polls)

        elif choice == 0:
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
