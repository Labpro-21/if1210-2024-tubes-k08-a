from utils.primordials import *
import os

root = os.path.dirname(__file__)
directory = os.path.join(root, '..', 'data')

def get_arr(filename: str, directory: str) -> list[list[str]]:
    # membuat array of array dari file csv
    res = []
    
    with open(os.path.join(directory, filename)) as f:
        lines = string_split(f.read(), "\n")
        for line in lines:
            array_push(res, string_split(line, ";"))
        array_push(res, "__EOP__")
    return res

def load_user() -> tuple[list[int], list[str], list[str], list[str], list[int]]:
    
    id_list = []
    username_list = []
    password_list = []
    role_list = []
    oc_list = []
    
    i = 1
    temp_user = get_arr("user.csv", directory)
    
    while temp_user[i] != "__EOP__":
        array_push(id_list, int(temp_user[i][0]))
        array_push(username_list, temp_user[i][1])
        array_push(password_list, temp_user[i][2])
        array_push(role_list, temp_user[i][3])
        array_push(oc_list, int(temp_user[i][4]))
        i += 1
    # user_list = [id_list, username_list, password_list, role_list, oc_list]
    return (id_list, username_list, password_list, role_list, oc_list)

def load_monster() -> tuple[list[int], list[str], list[int], list[int], list[int]]:
    
    id_list = []
    type_list = []
    atk_power_list = []
    def_power_list = []
    hp_list = []
    
    i = 1
    temp_monster = get_arr("monster.csv", directory)
    
    while temp_monster[i] != "__EOP__":
        array_push(id_list, int(temp_monster[i][0]))
        array_push(type_list, temp_monster[i][1])
        array_push(atk_power_list, int(temp_monster[i][2]))
        array_push(def_power_list, int(temp_monster[i][3]))
        array_push(hp_list, int(temp_monster[i][4]))
        i += 1
    # monster_list = [id_list, type_list, atk_power_list, def_power_list, hp_list]
    return (id_list, type_list, atk_power_list, def_power_list, hp_list)

def load_item_inventory() -> tuple[list[int], list[str], list[int]]:
    
    user_id_list = []
    type_list = []
    quantity_list = []

    i = 1
    temp_item_inventory = get_arr("item_inventory.csv", directory)
    
    while temp_item_inventory[i] != "__EOP__":
        array_push(user_id_list, int(temp_item_inventory[i][0]))
        array_push(type_list, temp_item_inventory[i][1])
        array_push(quantity_list, int(temp_item_inventory[i][2]))
        i += 1
    # item_inventory_list = [user_id_list, type_list, quantity_list]
    return (user_id_list, type_list, quantity_list)

def load_monster_inventory() -> tuple[list[int], list[int], list[int]]:
    
    user_id_list = []
    monster_id_list = []
    level_list = []

    i = 1
    temp_monster_inventory = get_arr("monster_inventory.csv", directory)
    
    while temp_monster_inventory[i] != "__EOP__":
        array_push(user_id_list, int(temp_monster_inventory[i][0]))
        array_push(monster_id_list, int(temp_monster_inventory[i][1]))
        array_push(level_list, int(temp_monster_inventory[i][2]))
        i += 1
    # monster_inventory_list = [user_id_list, monster_id_list, level_list]
    return (user_id_list, monster_id_list, level_list)

def load_item_shop() -> tuple[list[str], list[int], list[int]]:
    
    type_list = []
    stock_list = []
    price_list = []

    i = 1
    temp_item_shop = get_arr("item_shop.csv", directory)
    
    while temp_item_shop[i] != "__EOP__":
        array_push(type_list, temp_item_shop[i][0])
        array_push(stock_list, int(temp_item_shop[i][1]))
        array_push(price_list, int(temp_item_shop[i][2]))
        i += 1
    # item_shop_list = [type_list, stock_list, price_list]
    return (type_list, stock_list, price_list)

def load_monster_shop() -> tuple[list[int], list[int], list[int]]:
    
    monster_id_list = []
    stock_list = []
    price_list = []

    i = 1
    temp_monster_shop = get_arr("monster_shop.csv", directory)
    
    while temp_monster_shop[i] != "__EOP__":
        array_push(monster_id_list, int(temp_monster_shop[i][0]))
        array_push(stock_list, int(temp_monster_shop[i][1]))
        array_push(price_list, int(temp_monster_shop[i][2]))
        i += 1
    # monster_shop_list = [monster_id_list, stock_list, price_list]
    return (monster_id_list, stock_list, price_list)

# print("user:", load_user())
# print("monster:", load_monster())
# print("item_inventory:", load_item_inventory())
# print("monster_inventory:", load_monster_inventory())
# print("item_shop:", load_item_shop())
# print("monster_shop:", load_monster_shop())
