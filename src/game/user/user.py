from utils.primordials import *
from utils.coroutines import *
from utils.math import *
from game.state import *
from game.database import *
from game.monster import *
from game.inventory import *
from typing import Optional, Union, Callable

def _user_get(gameState: GameState, userId: int) -> UserSchemaType:
    userDatabase = gamestate_get_user_database(gameState)
    return database_get_entry_at(userDatabase, userId)

def _user_set(gameState: GameState, userId: int, modifier: Union[UserSchemaType, Callable[[UserSchemaType], UserSchemaType]]) -> UserSchemaType:
    userDatabase = gamestate_get_user_database(gameState)
    user = modifier(database_get_entry_at(userDatabase, userId)) if callable(modifier) else modifier
    database_set_entry_at(userDatabase, userId, user)
    return user

def _user_new(gameState: GameState) -> UserSchemaType:
    userDatabase = gamestate_get_user_database(gameState)
    userId = database_get_entries_length(userDatabase)
    user = UserSchemaType(
        id=userId,
        username=None,
        password=None,
        role=None,
        money=None,
    )
    database_set_entry_at(userDatabase, userId, user)
    return user

def _user_get_all_npcs(gameState: GameState) -> list[UserSchemaType]:
    userDatabase = gamestate_get_user_database(gameState)
    userEntries = database_get_entries(userDatabase)
    return array_filter(userEntries, lambda u, *_: u.role == "npc")

# Do NOT expose this function in __init__.py. See note in __init__.py
def __user_hash_password(password: str) -> str:
    pass 

def _user_is_logged_in(gameState: GameState) -> bool:
    return gamestate_get_user_id(gameState) is not None

def _user_get_current(gameState: GameState) -> Optional[UserSchemaType]:
    userId = gamestate_get_user_id(gameState)
    if userId is None:
        return None
    user_database = gamestate_get_user_database(gameState)
    return database_get_entry_at(user_database, userId)

def _user_register(state, args) -> None:
    if state is SuspendableInitial:
        gameState, console, new_username, new_password = args
        print, input, meta = console
        '''
        Prosedur untuk register user baru
        '''
        user_database = gamestate_get_user_database(gameState)
        user_entries = database_get_entries(user_database)
        # mengecek apakah user sedang login atau tidak
        if _user_is_logged_in(gameState):
            print("Anda sudah login, logout dulu untuk register!")
            return SuspendableReturn, None
        
        # input username baru
        # new_username: str = input("Masukan username: ")
            
        # mengecek apakah karakter dalam username valid
        user_false_input: bool = True
        valid_username: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_1234567890"
        
        for i in range (len(new_username)):
            for j in range (len(valid_username)):
                if new_username[i] != valid_username[j]:
                    user_false_input = True
                else:
                    user_false_input = False
                    break
            if user_false_input == True:
                break
            
        if user_false_input == True:
            print("Username hanya boleh berisi alfabet, angka, underscore, dan strip!")
            return SuspendableReturn, None
        else:
        # mengecek apakah username sudah ada di database   
            for i in range (len(user_entries)):
                if new_username == user_entries[i].username:
                    print(f"Username {txtplnm(new_username)} sudah terpakai, silahkan gunakan username lain!")
                    return SuspendableReturn, None

        # input password
        # new_password: str = input("Masukan password: ")
        
        # input pilihan monster starter
        availableMonsters = monster_get_all_monsters(gameState)
        availableMonsters = array_filter(availableMonsters, lambda m, *_: m.level == 1)
        availableMonsters = array_map(rand_uniq_int_array(0, len(availableMonsters), min(5, len(availableMonsters))), lambda i, *_: availableMonsters[i])
        print("Silakan pilih salah satu monster sebagai monster awalmu.")
        for availableMonster in availableMonsters:
            description = txtkv("F: ", availableMonster.family) + " "
            description += txtkv("L: ", availableMonster.level) + " "
            description += txtkv("HP: ", f"{availableMonster.healthPoints:.1f}") + " " # TODO: These properties do not include potion effects
            description += txtkv("ATK: ", f"{availableMonster.attackPower:.1f}") + " "
            description += txtkv("DEF: ", f"{availableMonster.defensePower:.1f}") + ""
            input(smnstr(availableMonster.name), description, id=availableMonster.id, selectable=True)
        meta(action="pushFlags")
        meta("selectableAllowEscape", False)
        selection = meta(action="select")
        return "choose_monster", gameState, console, new_username, new_password, selection
    if state == "choose_monster":
        gameState, console, new_username, new_password, selection = args
        print, input, meta = console
        meta(action="popFlags")
        
        # writing new user to database
        # id itu zero-based, jadi langsung pakai length() untuk mendapatkan id selanjutnya.
        user = _user_new(gameState)
        user = _user_set(gameState, user.id, namedtuple_with(user,
            username=new_username,
            password=new_password,
            role="agent",
            money=500
        ))
        
        monsterId = selection
        monster = monster_get(gameState, monsterId)
        inventoryMonster = inventory_monster_new(gameState)
        inventoryMonster = inventory_monster_set(gameState, inventoryMonster.id, namedtuple_with(inventoryMonster,
            ownerId=user.id,
            referenceId=monsterId,
            name=monster.name,
            experiencePoints=0,
            healthPoints=monster.healthPoints,
            attackPower=monster.attackPower,
            defensePower=monster.defensePower,
            activePotions=[],
        ))

        gamestate_set_user_id(gameState, user.id)

        meta(action="clear")
        print(f"Selamat datang Agent {txtplnm(new_username)}. Mari kita mengalahkan Dr. Asep Spakbor dengan {smnstr(inventoryMonster.name)}!")
        input("Lanjut", selectable=True)
        selection = meta(action="select")
        
        return SuspendableReturn, None, selection
    return SuspendableExhausted

def _user_login(gameState: GameState, username: str, password: str) -> None:
    '''
    Prosedur untuk login user
    '''
    user_database = gamestate_get_user_database(gameState)
    user_entries = database_get_entries(user_database)
    # mengecek apakah user sedang login atau tidak
    if _user_is_logged_in(gameState):
        print("Anda sudah login, logout dulu untuk login!")
        return
    
    # input username
    # username: str = input("Masukan username: ")
    
    # mencari apakah user ada
    user_DNE = True 
    for i in range (len(user_entries)):
        if username == user_entries[i].username:
            user_DNE = False
            user_index = i
            break
    
    # jika user yang diinput tidak ada, akan exit dari prosedur
    if user_DNE == True:
        print("")
        print("Username tidak terdaftar!")
        return
    
    # input password
    # password: str = input("Masukan password: ")
    
    # mengecek password benar atau tidak
    if password != user_entries[user_index].password: # salah
        print("")
        print("Password salah!")
        return
    else: # benar
        print(f'''
Selamat datang, Agent {txtplnm(username)}!
              ''')
        newly_logged_in_id = user_entries[user_index].id
        gamestate_set_user_id(gameState, newly_logged_in_id)

def _user_logout(gameState: GameState) -> None:
    '''
    Prosedur untuk logout user
    '''
    # mengecek apakah user sedang login atau tidak
    if gamestate_get_user_id(gameState) is None:
        print("Anda belum login, login dulu untuk logout!")
        return
    else:
        gamestate_set_user_id(gameState, None)
        print("Anda sukses logout")
        return
        
