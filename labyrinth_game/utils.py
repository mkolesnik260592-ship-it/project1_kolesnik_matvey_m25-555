from constants import ROOMS


def describe_current_room(game_state):
    #получаем данные о текущей комнате
    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]

    #выводим название комнаты в верхнем регистре
    print(f"== {current_room_name.upper()} ==")

    #выводим описание комнаты
    print(room_data['description'])

    #выводим предметы если они есть
    if room_data['items']:
        print("Заметные предметы:")
        for item in room_data['items']:
            print(f"  - {item}")

    #выводим доступные выходы
    print("Выходы:")
    for direction, room in room_data['exits'].items():
        print(f"  - {direction}: {room}")

    #сообщение о загадке
    if room_data['puzzle']:
        print("Здесь загадка (используй комманду solve).")

def solve_puzzle(game_state):
    """
    Решение головоломок
    """

    current_room_name = game_state['current_room']
    room_data = ROOMS[current_room_name]

    if room_data['puzzle'] == None:
        print("Загадок здесь нет")
        return
    else:
        question, correct_answer = room_data['puzzle']
        print(question)
        answer = input("Ваш ответ: ")
        if answer == correct_answer:
            room_data['puzzle'] = None
            print("Ура! Ответ правильный")
        else:
            print("Неверно, попробуйте снова")
