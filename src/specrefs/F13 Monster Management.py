data_monster =  [
["ID","Type","ATK Power","DEF Power","HP"],
[1,"Pikachow",125,10,600],
[2,"Bulbu",50,50,1200],
[3,"Zeze",300,10,100],
[4,"Zuko",100,25,800],
[5,"Chacha",80,30,700],
] 

# read_csv("monster.csv") # Membaca 
print("SELAMAT DATANG DI DATABASE PARA MONSTER !!!")
print("1. Tampilkan semua Monster")
print("2. Tambah Monster baru")
aksi = int(input("Pilih aksi : "))
if aksi == 1 :
    for row in data_monster :
       print(' | '.join(map(str, row))) 
    

elif aksi == 2:
    no = 5
    print("Memulai pembuatan Monster baru")
    type = input("Masukkan Type / Nama: ")
    if (type == "Pikachow") or (type == "Bulbu") or (type == "Bulbu") or (type == "Zeze") or (type == "Zuko") or (type == "Chaca"):
        print("Nama sudah terdaftar, coba lagi!")
      
    while True:
        no += 1
        try:
            ATKpower = int(input("Masukkan ATK Power : "))
            break
        except:
            print("Masukkan input berupa Integer, coba lagi!")    

    Def = int(input("Masukkan DEF Power : "))
    while 0<= Def <= 50:
        try:
            HP = int(input("Masukkan HP: ")) 
            break
        except:
            print("DEF Power harus bernilai 0-50, coba lagi!")

    print("Monster baru berhasil dibuat!")
    print(f"Type : {type}")
    print(f"ATK Power : {ATKpower}")
    print(f"DEF Power : {Def}")
    print(f"HP :{HP}")

    masukkan = input("Tambahkan Monster ke database (Y/N) : ")
    if masukkan == "Y":
        print("ID | Type | ATK Power | DEF Power | HP")
        new_monster = [no, type, ATKpower, Def, HP]
        new_data = data_monster.append(new_monster)
        for row in data_monster :
            print(' | '.join(map(str, row)))