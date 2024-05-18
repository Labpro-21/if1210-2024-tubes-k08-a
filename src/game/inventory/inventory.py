def read_csv(file_name):
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            row = custom_split(line.strip())
            data.append(row)
    return data

def custom_split(line, delimiter=';'):
    parts = []
    current_part = ''
    inside_quotes = False

    for char in line:
        if char == delimiter and not inside_quotes:
            parts.append(current_part)
            current_part = ''
        elif char == '"':
            inside_quotes = not inside_quotes
        else:
            current_part += char

    parts.append(current_part)
    return parts

read_csv("item_inventory.csv")
read_csv("monster_inventory.csv")
read_csv("database_user.csv")

def inventory() :
    x = 1
    print(f"============ INVENTORY LIST (User ID: {gamestate_get_user_id()}) ============")
    print(f" Jumlah O.W.C.A. Coin-mu sekarang {gamestate_get()}.")
    for monster in monsters:
        print(f"{x}. Monster      (Name: {gamestate_get()}, Lvl: {gamestate_get()}, HP: {gamestate_get()})")
        x += 1

if input == {}:# untuk monster
    print("Monster")
    print(f"Name      : {gamestate_get()}")
    print(f"ATK Power : {gamestate_get()}")
    print(f"DEF Power : {gamestate_get()}")
    print(f"HP        : {gamestate_get()}")
    print(f"Level     : {gamestate_get()}")

if input == {}:
    print("Potion")
    print(f"Type      : {gamestate_get()}")
    print(f"Quantity  : {gamestate_get()}")