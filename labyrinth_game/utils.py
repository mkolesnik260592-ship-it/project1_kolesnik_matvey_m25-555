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

    if room_data['puzzle'] is None:
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

def attempt_open_treasure(game_state):
    """
    Реализация механики победы
    """


    current_room_name = game_state['current_room']
    inventory = game_state['player_inventory']

    if current_room_name != 'treasure_room':
        return

    if 'treasure_chest' not in ROOMS['treasure_room']['items']:
        print("Сундук уже открыт.")
        return

    if 'treasure_key' in inventory:
        ROOMS['treasure_room']['items'].remove('treasure_chest')
        print("Поздравляем с победой!!! Вы добыли сокровище!")
        game_state['game_over'] = True
    else:
        print("Сундук заперт. Хотите попробовать ввести код?")
        solution = input("Ваш ответ (Да/Нет): ")
        if solution.lower() not in ['да', 'yes']:
            print("Вы отступаете от сундука")
            return
        else:
            chest_code = input("Введите код: ")
            right_code = ROOMS['treasure_room']['puzzle'][1]
            if chest_code == right_code:
                ROOMS['treasure_room']['items'].remove('treasure_chest')
                print("Поздравляем м победой!!! Вы добыли сокровище")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остается запертым.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
