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

from constants import ROOMS
from utils import describe_current_room

def move_player(game_state, direction):

    room_data = ROOMS[current_room_name] #получение данных комнаты

    if direction in room_data['exits']: #Проверка наличия направления
        new_room = room_data['exits'][direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1 #текущее количество шагов

        describe_current_room(game_state) #показывает текущую комнату

    else:
        print("Нельзя пройти в этом направлении.")

def take_item(game_state, item_name):
    current_room_name = game_state['current_room'] #название текущей комнаты
    room_data = ROOMS[current_room_name]

    if item_name in room_data['items']: #проверка наличия предметов в комнате
        game_state['player_inventory'].append(item_name) #добавление в инвентарь
        room_data['items'].remove(item_name) #удаление предмета из комнаты
        print(f'Вы подняли: {item_name}')
    else:
        print('Такого предмета здесь нет')
