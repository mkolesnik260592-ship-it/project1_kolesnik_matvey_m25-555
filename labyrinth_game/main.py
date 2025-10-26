#!/usr/bin/env python3

from player_actions import get_input, move_player, show_inventory, take_item, use_item
from utils import describe_current_room, solve_puzzle


def process_command(game_state, command):
    parts = command.split() #делим комманду
    player_command = parts[0] if parts else "" #получение команды
    argument = " ".join(parts[1:]) if len(parts) > 1 else "" #получение аргумента

    match player_command:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go":
            move_player(game_state, argument)
        case "take":
            take_item(game_state, argument)
        case "use":
            use_item(game_state, argument)
        case "solve":
            solve_puzzle(game_state)
        case "quit":
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Попробуйте: look, inventory, go <направление>, take <предмет>, use <предмет>, solve, quit")


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

        if command in ["quit", "exit"]:
            print("Спасибо за игру!")
            break

        process_command(game_state, command)


if __name__ == "__main__":
    main()
