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
read_csv("monster.csv")
read_csv("user.csv")

mons_id = read_csv("monster_inventory.csv")
mons_Lvl = read_csv("monster_inventory.csv")
mons = read_csv("monster.csv")
user_id = read_csv("user.csv")
baca_oc = read_csv("user.csv")
item_inv = read_csv("item_inventory.csv")

def show_mons_inv():
    for i in range (1, len(mons_id)):
        id = mons_id[i][0]
        m_type = mons[i][1]
        hp = mons[i][4]
        oc = baca_oc[i][4]
        m_lvl = mons_Lvl[i][2]
        if gamestate_get_user_id() == id:
            print(f"============ INVENTORY LIST (User ID: {id}) ============")
            print(f" Jumlah O.W.C.A. Coin-mu sekarang {oc}.")
            for monster in len(mons_id):
                print(f"{i}. Monster      (Name: {m_type}, Lvl: {m_lvl}, HP: {hp})")

def show_id_potion():
    for j in range (len(mons_id+1),len(mons_id) + len(item_inv)):
        id_1 = item_inv[j][0]
        type_1 = item_inv[j][0]
        Qty = item_inv[j][1]
        if gamestate_get_user_id() == id_1:
            print(f"{j}. Potion       (Type: {type_1}, Qty: {Qty})")

input1 = int(input())

def mons_inv_detail():
    for i in range (1, len(mons_id)):
        id = mons_id[i][0]
        m_type = mons[i][1]
        atk_power = mons[i][2]
        def_power = mons[i][3]
        hp = mons[i][4]
        m_lvl = mons_Lvl[i][2]
        for i in range (1, len(mons_id)) :
            if gamestate_get_user_id() == id:
                if input1 == mons_id[i][2]:
                    print("Monster")
                    print(f"Name      : {m_type}")
                    print(f"ATK Power : {atk_power}")
                    print(f"DEF Power : {def_power}")
                    print(f"HP        : {hp}")
                    print(f"Level     : {m_lvl}")

def show_potion_detail():
    for j in range (len(mons_id+1),len(mons_id) + len(item_inv)):
        id_1 = item_inv[j][0]
        type_1 = item_inv[j][0]
        Qty = item_inv[j][1]
        for j in range (len(mons_id)+1,len(mons_id) + len(item_inv)):
            if gamestate_get_user_id() == id_1:
                if input1 == j:
                    print("Potion")
                    print(f"Type      : {type_1}")
                    print(f"Quantity  : {Qty}")
