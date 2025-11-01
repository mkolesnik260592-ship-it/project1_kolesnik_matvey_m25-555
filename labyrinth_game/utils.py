import math

from labyrinth_game.constants import ROOMS


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
        accepted_answers = [correct_answer]
        if current_room_name == 'hall':
            accepted_answers.extend(['десять', 'Десять', 'Ten', 'ten'])
        elif current_room_name == 'treasure_room':
            accepted_answers.extend(['десять', 'Десять', 'ten', 'Ten'])
        elif current_room_name == 'garden':
            accepted_answers.extend(['пять', 'Пять', 'Five', 'five'])

        if answer in accepted_answers:
            room_data['puzzle'] = None
            print("Ура! Ответ правильный")
            if current_room_name == 'hall':
                game_state['player_inventory'].append('magic_dust')
                print("Вы получили magic_dust")
            elif current_room_name == 'library':
                game_state['player_inventory'].append('ancient_book_translator')
                print("Вы получили ancient_book_translator")
            elif current_room_name == 'garden':
                game_state['player_inventory'].append('pot')
                print("Вы получили pot")
            elif current_room_name == 'secret_chamber':
                game_state['player_inventory'].append('rusty_key')
                print("Вы получили rusty_key")

        else:
            print("Неверно, попробуйте снова")
            if current_room_name == 'trap_room':
                trigger_trap(game_state)

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
                print("Поздравляем с победой!!! Вы добыли сокровище")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остается запертым.")

def show_help(COMMANDS):
    """
    Вывод справки
    """
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f'  {command:<16} - {description}')

def pseudo_random(seed, modulo):
    """
    Вычисление псевдо рандома
    """

    value = math.sin(seed*12.9898)
    value *= 43758.5453
    fractional_part = value - math.floor(value)
    scaled = int(fractional_part * modulo)
    return scaled

def trigger_trap(game_state):
    """
    Функция срабатывания ловушки
    """
    print("Ловушка активирована! Пол стал дрожать...")

    if len(game_state['player_inventory']) > 0:
        random_index = pseudo_random(seed=game_state['steps_taken'], modulo=len(game_state['player_inventory']))
        item = game_state['player_inventory'][random_index]
        game_state['player_inventory'].pop(random_index)
        print(f'Вы потеряли предмет: {item}')
    else:
        damage = pseudo_random(seed=game_state['steps_taken'], modulo=10)
        if damage < 3:
            print("Игрока постигла ужасная участь. Игра окончна.")
            game_state['game_over'] = True
        else:
            print("Игрок жив (но напуган)")

def random_event(game_state):
    """
    Генерация рандомного события
    """
    if pseudo_random(seed=game_state['steps_taken'], modulo=10) == 0:
        event_type = pseudo_random(seed=game_state['steps_taken'] + 1, modulo=3)
        if event_type == 0:
            print("Вы нашли монетку")
            current_room_name = game_state['current_room']
            ROOMS[current_room_name]['items'].append('coin')
        elif event_type == 1:
            print("Вы слышите странный шорох из темного угла")
            if 'sword' in game_state['player_inventory']:
                print("который прекратился, как только вы достали меч")
            else:
                print("который заставляет вас вспомнить все молитвы и шептать их себе под нос.")
        elif event_type == 2:
            if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
                trigger_trap(game_state)
