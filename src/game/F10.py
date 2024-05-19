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

def show_id_mons():
    for i in range (1, len(mons_shop)):
        id = mons_shop[i][0]
        type = mons[i][1]
        atk = mons[i][2]
        defence = mons [i][3]
        hp = mons [i][4]
        stok = mons_shop [i][1]
        price = mons_shop [i][2]
        print (f"{id}  |{type}   |{atk}    |{defence}   |{hp}   |{stok}   |{price}  ")

def show_id_pot():
    for j in range (1, len(item_Shop)):
        id_1 = j
        type_1 = item_Shop[j][0]
        stok_1 = item_Shop[j][1]
        harga_1 = item_Shop[j][2]
        print(f"{id_1} |{type_1} potion         |{stok_1}   |{harga_1}")

def beli_mons():
    for i in range (1, len(mons_shop)):
        id = mons_shop[i][0]
        type = mons[i][1]
        type_inv_id = mons_inv[i][1]
        stok = mons_shop [i][1]
        price = mons_shop [i][2]
        oc = baca_oc[pilih_id][4]
        if aksi_beli_monster == id:
            oc = int(oc)
            price = int(price)
            stok = int(stok)
            if aksi_beli_monster == type_inv_id:
                print("Monster sudah ada di inventory kamu :), transaksi dibatalkan")
            else:
                if stok >= 1:
                    if oc >= price:
                        print(f"kamu berhasil membeli {type}, dan {type} telah disimpan di inventory.")
                        print(f"Sisa O.C kamu {oc-price}")
                        oc = oc - price
                        oc = str(oc)
                        baca_oc[pilih_id][4] = oc
                        stok -= 1
                        stok = str(stok)
                        mons_shop [i][1] = stok
                    elif oc < price:
                        print("O.C kamu kurang :(")
                else:
                    print("Stok monster habis")
def beli_potion():
    for j in range (1, len(item_Shop)):
        id_1 = j
        type_1 = item_Shop[j][0]
        stok_1 = item_Shop[j][1]
        harga_1 = item_Shop[j][2]
        oc = baca_oc[pilih_id][4]
        if aksi_beli_potion == id_1:
            oc = int(oc)
            harga_1 = int(harga_1)
            stok_1 = int(stok_1)
            jumlah = int(jumlah_beli_potion * harga_1)
            if stok_1 >= 1:
                if oc >= harga_1:
                    print(f"kamu berhasil membeli {type_1}")
                    print(f"Sisa O.C kamu {oc-jumlah}, sebanyak {jumlah_beli_potion}")
                    oc = oc - jumlah
                    oc = str(oc)
                    baca_oc[pilih_id][4] = oc
                    stok_1 -= 1
                    stok_1 = str(stok_1)
                    item_Shop[j][1] = stok_1
                elif oc == harga_1:
                    beli_ga = str(input("O.C kamu pas-pasan untuk beli potion... mau lanjut beli? (Y/N)"))
                    if beli_ga == "Y" or beli_ga == "y":
                        print(f"kamu berhasil membeli {type_1}")
                        print(f"Sisa O.C kamu {oc-jumlah}, sebanyak {jumlah_beli_potion}")
                        oc = oc - jumlah
                        oc = str(oc)
                        baca_oc[pilih_id][4] = oc
                        stok_1 -= 1
                        stok_1 = str(stok_1)
                        item_Shop[j][1] = stok_1
                    elif beli_ga =="N" or beli_ga =="n":
                        print("Okay transaksi dibatalkan, selamat menabung!!")
                elif oc < harga_1:
                    print("O.C kamu kurang :(")
            else:
                ("Stok potion habis")

                
# Example usage:
print("<<<SHOP>>>")
print("\nIrassahaimase! Selamat datang di SHOP!!\n")
read_csv("item_inventory.csv")
read_csv("item_shop.csv")
read_csv("user.csv")
read_csv("monster_shop.csv")
read_csv("monster.csv")

item_Shop = read_csv("item_shop.csv")
mons = read_csv("monster.csv")
item_inv = read_csv("item_inventory.csv")
mons_shop = read_csv("monster_shop.csv")
mons_inv = read_csv("monster_inventory.csv")
user_id = read_csv("user.csv")
baca_oc = read_csv("user.csv")
x = 0

oc = baca_oc[pilih_id][4]

while x == 0:
    aksi = str(input("Pilih aksi (lihat/beli/keluar): "))
    if aksi == "keluar":
        print("Mr. Yanto bilang makasih, belanja lagi ya nanti :)")
        x += 1
    elif aksi == "lihat":    
        aksi_2 = str(input(f"Mau {aksi} apa (monster/potion): "))
        if aksi_2 == "monster":
            print ("ID |Type      |ATK Power  |DEF Power |HP  |Stok  |Harga  ")
            show_id_mons()
        elif aksi_2 == "potion":
            print("ID |Type      |Stok    |Harga")
            show_id_pot()
    elif aksi == "beli":
        oc = baca_oc[pilih_id][4]
        print(f"jumlah O.W.C.A coin-mu sekarang {oc}")
        aksi_3 = str(input("Mau beli apa? (monster/potion): "))
        if aksi_3 == "monster" or aksi_3 == "Monster" or aksi_3 == "MONSTER":
            aksi_beli_monster = str(input("Masukkan id monster: "))
            beli_mons()
        elif aksi_3 == "potion" or aksi_3 == "Potion" or aksi_3 == "POTION":
            aksi_beli_potion = int(input("Masukkan id potion: "))
            jumlah_beli_potion = int(input("Masukkan jumlah potion: "))
            beli_potion()