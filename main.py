from datetime import date

poll_title = "Выбор темы для корпоратива"
author = "Иван Петров"
created_date = date(2026, 9, 15)
is_active = False

choices = ["Караоке", "Боулинг", "Квест-комната", "Ресторан"]

def get_poll_status(is_active):
    if is_active:
        return "Голосование активно"
    return "Голосование завершено"

def get_options(choices):
    if len(choices) == 0:
        print('У этого опроса нет вариантов ответа')
    else:
        for i in range(len(choices)):
            print(i+1, '.', choices[i])

print(f"Голосование: {poll_title}")
print(f"Автор: {author}")
print(f"Дата создания: {created_date}")
print(f"Варианты ответов: {', '.join(choices)}")
print(get_poll_status(is_active))
get_options(choices)