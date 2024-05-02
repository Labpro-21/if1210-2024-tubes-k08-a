# Program python ini masih sangat belum siap diimplementasi dalam main
# Belum dikoneksi dengan database
# Untuk UI perlu dilakukan di program yang mengeksekusi fungsi-fungsi di bawah, katakan program ini bernama "executor"
# Untuk mengetahui apakah user sudah login/tidak harus dilakukan dicek dalam "executor"
# Fitur logout juga harus diimplementasi dalam "executor" 

# Saat ini baru ada fungsi untuk register dan login

def register() -> None:
    
    # username input
    user_false: bool = True
    registered_users: list[str] = ["john", "dan", "jane"] # untuk sekarang menggunakan array sebagai database untuk ujicoba
    valid_username: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_1234567890"
    new_username: str = input("Masukan username: ")
        
    # mengecek apakah karakter dalam username valid
    for i in range (len(new_username)):
        for j in range (len(valid_username)):
            if new_username[i] != valid_username[j]:
                user_false = True
            else:
                user_false = False
                break
        if user_false == True:
            break
    if user_false == True:
        print("")
        print("Username hanya boleh berisi alfabet, angka, underscore, dan strip!")
        return
    else:
    # mengecek apakah username sudah ada di database   
        for i in range (len(registered_users)):
            if new_username == registered_users[i]:
                print("")
                print(f"Username {new_username} sudah terpakai, silahkan gunakan username lain!")
                # user_false = True
                return
            # else:
            #     user_false = False
    
    # input password
    password: str = input("Masukan password: ")
    
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
    # write new_id, new_username, password, starter_choice, new_oc to database
    
# register()

def login() -> None:
    valid_users: list[str] = ["john", "dan", "jane"] # untuk sekarang menggunakan array sebagai database untuk ujicoba
    password_valid: list[str] = ["haha", "hehe", "hoho"]
    username: str = input("Masukan username: ")
    
    # mengecek apakah username ada di database  
    user_DNE = True 
    for i in range (len(valid_users)):
        if username == valid_users[i]:
            user_DNE = False
            index_user = i
            break
    
    if user_DNE == True:
        print("")
        print("Username tidak terdaftar!")
        return
    
    # input password
    password: str = input("Masukan password: ")
    if password != password_valid[index_user]:
        print("")
        print("Password salah!")
        return
    else:
        print(f'''
Selamat datang, Agent {username}!
Masukkan command “help” untuk daftar command yang dapat kamu panggil.
              ''')

# login()

    
        
