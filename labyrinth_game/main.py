#!/usr/bin/env python3

from constants import ROOMS
from utils import describe_current_room
from player_actions import show_inventory, get_input

def main():
   # Создаем состояние игры
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input()

        if command == "quit":
            print("Спасибо за игру!")
            break
        elif command == "inventory":
            show_inventory(game_state)
        else:
            print("Неизвестная команда. Попробуйте 'inventory' или 'quit'.")

if __name__ == "__main__":
    main()
