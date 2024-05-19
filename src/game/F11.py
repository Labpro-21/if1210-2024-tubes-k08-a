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

# Example usage:
print("\nSelamat datang di Lab Dokter Asep !!!\n")
read_csv("monster_inventory.csv")
read_csv("monster.csv")
read_csv("user.csv")

tabel_Mons = read_csv("monster.csv")
tabel_Mons_inv = read_csv("monster_inventory.csv")
baca_user_id = read_csv("user.csv")
baca_oc = read_csv("user.csv")

user_database = gamestate_get_user_id(gameState) #masih harus diperbaiki karena harus cek id mana yang login
user_entry = database_get_entries_at(user_database, user_id)
oc = user_entry.money

j=1
print("============ MONSTER LIST ============")
for i in range (len(tabel_Mons_inv)):
    if tabel_Mons_inv[i][0] == user_database  :
        level = tabel_Mons_inv[i][2]
        id = tabel_Mons_inv[i][1]
        for i in range (len(tabel_Mons)):
            if id == tabel_Mons[i][0]:
                print(f"{j}. {tabel_Mons[i][1]} (level: {level}) ") 
                j += 1

print ("============ UPGRADE PRICE ============")
print ("1. Level 1 -> Level 2: 300 OC")
print ("2. Level 2 -> Level 3: 500 OC")
print ("3. Level 3 -> Level 4: 800 OC")
print ("4. Level 4 -> Level 5: 1000 OC")


harga = [0,300,500,800,1000]
choice = int(input("Pilih monster: "))
j = 0
for i in range (len(tabel_Mons_inv)):
    if tabel_Mons_inv[i][0] == user_database  :
        level = tabel_Mons_inv[i][2]
        id = tabel_Mons_inv[i][1]
        for k in range (len(tabel_Mons)):
            if id == tabel_Mons[k][0]:
                j += 1
                if choice == j:
                    levels = int(level)
                    levelb = int(level)
                    ocs = int(oc)
                    if levels >= 5:
                        print("Maaf, monster yang Anda pilih sudah memiliki level maksimum")
                    else:
                        print(f"{tabel_Mons[j][1]} akan di-upgrade ke level {levels+1}")
                        print(f"Harga untuk melakukan upgrade {tabel_Mons[j][1]} adalah {harga[levels]} OC")
                        lanjut_upgrade = str(input("Lanjutkan upgrade (Y/N): "))
                        if lanjut_upgrade == "Y" or lanjut_upgrade == "y":
                            if ocs >= harga[levels]:
                                print(f"Selamat, {tabel_Mons[j][1]} berhasil di-upgrade ke level {levels+1} ")
                                sisa_ocs = ocs - harga[levelb]
                                print(f"sisa OWCA kamu :{sisa_ocs}")
                                levels += 1
                                levels = str(levels)
                                sisa_ocs = str(sisa_ocs)
                                baca_oc [i][4] = sisa_ocs
                                tabel_Mons_inv[i][2] = level
                            else:
                                print(f"OC Anda kurang, maka monster {tabel_Mons[j][1]} tidak dapat di-upgrade :(")
                        elif lanjut_upgrade == "N" or lanjut_upgrade == "n":
                            print(f"Monster {tabel_Mons[j][1]} tidak jadi di-upgrade")
                        else:
                            print("Mohon maaf command yang anda masukan salah")