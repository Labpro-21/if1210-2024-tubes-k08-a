from utils.primordials import *
from game.state import *
from game.database import *
from typing import Optional, Union, Callable

def _user_get(gameState: GameState, userId: int) -> UserSchemaType:
    userDatabase = gamestate_get_user_database(gameState)
    return database_get_entry_at(userDatabase, userId)

def _user_set(gameState: GameState, userId: int, modifier: Union[UserSchemaType, Callable[[UserSchemaType], UserSchemaType]]) -> UserSchemaType:
    userDatabase = gamestate_get_user_database(gameState)
    user = modifier(database_get_entry_at(userDatabase, userId)) if callable(modifier) else modifier
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

def _user_register(gameState: GameState, new_username: str, new_password: str) -> None:
    '''
    Prosedur untuk register user baru
    '''
    user_database = gamestate_get_user_database(gameState)
    user_entries = database_get_entries(user_database)
    # mengecek apakah user sedang login atau tidak
    if _user_is_logged_in(gameState):
        print("Anda sudah login, logout dulu untuk register!")
        return
    
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
        return
    else:
    # mengecek apakah username sudah ada di database   
        for i in range (len(user_entries)):
            if new_username == user_entries[i].username:
                print(f"Username {new_username} sudah terpakai, silahkan gunakan username lain!")
                return

    # input password
    # new_password: str = input("Masukan password: ")
    
    # input pilihan monster starter
    monster_false: bool = True
    input_salah: bool = False
    while monster_false == True:
        if input_salah == True:
            print("Pilihan hanya '1', '2', atau '3'! Pilih salah satu!\n")
        print('''
Silakan pilih salah satu monster sebagai monster awalmu.
1. Monster1
2. Monster2
3. Monster3
Input angka saja, contoh: input '1' untuk memilih Monster1
            ''')
        starter_num: str = input("Monster pilihanmu: ")
        if starter_num == "1" or starter_num == "2" or starter_num == "3":
            monster_false = False
        else:
            input_salah = True

    starter_choice: str
    if starter_num == '1':
        starter_choice = "Monster1"
    elif starter_num == '2':
        starter_choice = "Monster2"
    else:
        starter_choice = "Monster3"
        
    print(f"Selamat datang Agent {new_username}. Mari kita mengalahkan Dr. Asep Spakbor dengan {starter_choice}!")
    
    # writing new user to database
    # id itu zero-based, jadi langsung pakai length() untuk mendapatkan id selanjutnya.
    new_id = database_get_entries_length(user_database)
    database_set_entry_at(user_database, new_id, 
                          UserSchemaType(id = new_id, 
                                         username = new_username,
                                         password = new_password,
                                         role = "agent",
                                         money = 0))
    gamestate_set_user_id(gameState, new_id)
    return

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
Selamat datang, Agent {username}!
Masukkan command “help” untuk daftar command yang dapat kamu panggil.
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
        
