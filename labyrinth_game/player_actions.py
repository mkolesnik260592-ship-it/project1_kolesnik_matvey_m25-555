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
