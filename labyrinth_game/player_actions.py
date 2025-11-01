from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    """
    Отображает содержимое инвентаря игрока
    """
    inventory = game_state['player_inventory']

    if not inventory:  # если инвентарь пуст
        print("Инвентарь пуст.")
    else:
        print("Инвентарь:")
        for item in inventory:
            print(f"  - {item}")

def get_input(prompt="> "):
    """
    Получает ввод от пользователя с обработкой ошибок
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """
    Реализует прередвижение
    """
    current_room_name = game_state['current_room'] #название текущей комнаты
    room_data = ROOMS[current_room_name] #получение данных комнаты

    if direction in room_data['exits']: #Проверка наличия направления
        new_room = room_data['exits'][direction]
        if new_room == 'treasure_room': # проверка наличия rusty_key для входа в treasure_room
            if 'rusty_key' not in game_state['player_inventory']:
                print("Чтобы открыть эту дверь, нужен ключ.")
                return
            else:
                print("Вы открыли дверь ржавым ключем и попали в сокровищницу!!!")
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1 #текущее количество шагов
        describe_current_room(game_state) #показывает текущую комнату
        random_event(game_state) # Генерация рандомного события
    else:
        print("Нельзя пройти в этом направлении.")

def take_item(game_state, item_name):
    """
    Пополнение инвентаря
    """
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    current_room_name = game_state['current_room'] #название текущей комнаты
    room_data = ROOMS[current_room_name]

    if item_name in room_data['items']: #проверка наличия предметов в комнате
        game_state['player_inventory'].append(item_name) #добавление в инвентарь
        room_data['items'].remove(item_name) #удаление предмета из комнаты
        print(f'Вы подняли: {item_name}')
    else:
        print('Такого предмета здесь нет')

def use_item(game_state, item_name):
    """
    Проверка на наличие предмета, уникальное дейсвие для предмета
    """
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета")
        return

    match item_name:
        case 'torch':
            print("Стало светлее")
        case 'sword':
            print("Вы стали гораздо увереннее")
        case 'bronze_box':
            if 'rusty_key' in game_state['player_inventory']:
                print("Пусто")
            else:
                game_state['player_inventory'].append('rusty_key')
                game_state['player_inventory'].remove('bronze_box')
        case _:
            print("Вы не знаете что с этим делать")
