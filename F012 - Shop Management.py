print("Selamat datang, {user}")

aksi = input("Pilih aksi (lihat/tambah/ubah/hapus/keluar):" )

if aksi == "lihat":
     lihat = input("Mau lihat apa? (monster/potion):")
elif aksi == "tambah":
     nambah = input("Mau nambahin apa? (monster/potion): ")
elif aksi == "ubah":
     ubah = input("Mau ngubah apa? (monster/potion):")
elif aksi == "hapus":
     hapus = input("Mau hapus apa? (monster/potion):")
else :
     print("Dadah {user}, sampai jumpa di lain waktu!")

if (aksi == "lihat") and (lihat == "monster"):
    monsters =  [
["ID","Type","ATK Power","DEF Power","HP","Stok", "Harga"],
[1,"Pikachow",125,10,600,10,500],
[2,"Bulbu",50,50,1200,4,700],
[3,"Zeze",300,10,100,3,300],
[4,"Zuko",100,25,800,8,550],
[5,"Chacha",80,30,700,7,600],
]
    for row in monsters:
        print("|".join(map(str,row)))
    #read csv ("monster.csv")
    aksi = input("Pilih aksi (lihat/tambah/ubah/hapus/keluar):" )

elif (aksi == "lihat") and (lihat == "potion"):
    item_shops = [
["ID", "Type", "Stok", "Harga"],
[1, "Strength Potion", 10, 50],
[2, "Resilience", "Potion", 5, 30],
[3, "Healing Potion", 3, 20],
]
    for row in item_shops:
        print("|".join(map(str,row)) )

    aksi = input("Pilih aksi (lihat/tambah/ubah/hapus/keluar):" )

elif (aksi == "tambah") and (nambah == "monster"):
    monsters =  [
["ID","Type","ATK Power","DEF Power","HP"],
[1,"Pikachow",125,10,600],
[2,"Bulbu",50,50,1200],
[3,"Zeze",300,10,100],
[4,"Zuko",100,25,800],
[5,"Chacha",80,30,700],
] 
    for row in monsters:
        print("|".join(map(str,row)))
    id = int(input("Masukkan id monster: "))
    stokAwal = int(input("Masukkan stok awal: "))
    harga = int(input("Masukkan harga: "))
    if (id == 1) :
        new0 = [id, stokAwal, harga]
        monsters[0] = new0 #menambah ID 1
        for row in monsters:
            print("Pikachow berhasil ditambahkan ke dalam shop")

    elif (id == 2):
        new1 = [id, stokAwal, harga]
        monsters[1] = new1 #menambah ID 2
        for row in monsters:        
            print("Bulbu berhasil ditambahkan ke dalam shop!")

    elif (id == 3):
        new2 = [id, stokAwal, harga]
        monsters[2] = new2 #menambah ID 3
        for row in monsters:
            print("Zeze berhasil ditambahkan ke dalam shop!")

    elif (id == 4):
        new3 = [id, stokAwal, harga]
        monsters[3] = new3 #menambah ID 4
        for row in monsters:        
            print("Zuko berhasil ditambahkan ke dalam shop!")
        
    elif (id == 5):
        new4 = [id, stokAwal, harga]
        monsters[4] = new4 #menambah ID 5
        for row in monsters:        
            print("Chacha berhasil ditambahkan ke dalam shop!")
    
    aksi = input("Pilih aksi (lihat/tambah/ubah/hapus/keluar):" )


elif (aksi == "tambah") and (nambah == "potion"):
    item_shops = [
["ID", "Type", "Stok", "Harga"],
[1, "Strength Potion", 10, 50],
[2, "Resilience", "Potion", 5, 30],
[3, "Healing Potion", 3, 20],
]
    for row in item_shops:
        print("|".join(map(str,row)) )
    id = int(input("Masukkan id : "))
    stokAwal = int(input("Masukkan stok awal: "))
    harga = int(input("Masukkan harga: "))  
    if id == 1:
         New0 = [id, stokAwal, harga]
         item_shops[0] = New0 
         for row in item_shops: #menambah ID 1
            print("Strength Potion telah berhasil ditambahkan ke dalam shop!")
    elif id == 2:
         New1 = [id, stokAwal, harga]
         item_shops[1] = New1 
         for row in item_shops: #menambah ID 2        
            print("Resilience Potion telah berhasil ditambahkan ke dalam shop!")
    elif id == 3:
         New2 = [id, stokAwal, harga]
         item_shops[2] = New2
         for row in item_shops: #menambah ID 1         
            print("Healing Potion telah berhasil ditambahkan ke dalam shop!")

    aksi = input("Pilih aksi (lihat/tambah/ubah/hapus/keluar):" )

elif (aksi == "ubah") and (ubah == "monster"):
    monsters =  [
["ID","Type","ATK Power","DEF Power","HP","Stok", "Harga"],
[1,"Pikachow",125,10,600,10,500],
[2,"Bulbu",50,50,1200,4,700],
[3,"Zeze",300,10,100,3,300],
[4,"Zuko",100,25,800,8,550],
[5,"Chacha",80,30,700,7,600],
]
    for row in monsters:
        print("|".join(map(str,row)))
    id = int(input("Masukkan id monster: "))
    stokBaru = int(input("Masukkan stok baru: "))
    hargaBaru = input("Masukkan harga baru: ")

    if id == 1 : 
        baru0 = [id, stokBaru, hargaBaru]
        monsters[0] = baru0 #mengubah ID 1
        for row in monsters:           
            if hargaBaru != '':
                print(f"Pikachow telah berhasil diubah dengan stok baru sejumlah {stokBaru}!")
            elif hargaBaru == hargaBaru:
                print(f"Pikachow telah berhasil diubah dengan stok baru sejumlah {stokBaru} dan dengan harga {hargaBaru}!")
    elif id == 2 :
        baru1 = [id, stokBaru, hargaBaru]
        monsters[1] = baru1 #mengubah ID 2
        for row in monsters:
            if hargaBaru == '':        
                print(f"Bulbu telah berhasil diubah dengan stok baru sejumlah {stokBaru} !")
            elif hargaBaru == hargaBaru:
                print(f"Bulbu telah berhasil diubah dengan stok baru sejumlah {stokBaru} dan dengan harga {hargaBaru}!")

    elif id == 3 :
        baru2 = [id, stokBaru, hargaBaru]
        monsters[2] = baru2 #mengubah ID 3
        for row in monsters:
            if hargaBaru == '':  
                print(f"Zeze telah berhasil diubah dengan stok baru sejumlah {stokBaru}!")
            elif hargaBaru == hargaBaru:
                print(f"Zeze telah berhasil diubah dengan stok baru sejumlah {stokBaru} dan dengan harga {hargaBaru}!")
     
    elif id == 4 :
        baru3 = [id, stokBaru, hargaBaru]
        monsters[3] = baru3 #mengubah ID 4
        for row in monsters:
            if hargaBaru == '':  
                print(f"Zuko telah berhasil diubah dengan stok baru sejumlah {stokBaru}!")
            elif hargaBaru == hargaBaru :
                print(f"Zuko telah berhasil diubah dengan stok baru sejumlah {stokBaru} dan dengan harga {hargaBaru}!")
     
    elif id == 5:
        baru4 = [id, stokBaru, hargaBaru]
        monsters[4] = baru4 #mengubah ID 5
        for row in monsters:
            if hargaBaru == '':  
                print(f"Chacha telah berhasil diubah dengan stok baru sejumlah {stokBaru}!")
            elif hargaBaru == hargaBaru:
                print(f"Chaca telah berhasil diubah dengan stok baru sejumlah {stokBaru} dan dengan harga {hargaBaru}!")

elif (aksi == "ubah") and (ubah == "potion"):
    item_shops = [
["ID", "Type", "Stok", "Harga"],
[1, "Strength Potion", 10, 50],
[2, "Resilience", "Potion", 5, 30],
[3, "Healing Potion", 3, 20],
]
    for row in item_shops:
        print("|".join(map(str,row)) )
    id = int(input("Masukkan id potion: "))
    stokBaru = input("Masukkan stok baru: ")
    hargaBaru = int(input("Masukkan harga baru: "))
    
    if id == 1 :
        Baru0 = [id, stokBaru, hargaBaru]
        item_shops[0] = Baru0 #mengubah ID 1
        for row in item_shops:
            if stokBaru == '':
                print(f"Strength Potion telah berhasil diubah dengan harga baru {hargaBaru}!")
            elif stokBaru == stokBaru :
                print(f"Strength Potion telah berhasil diubah dengan stok baru sejumlah {stokBaru} dengan harga baru {hargaBaru}")
    elif id == 2 :
        Baru1 = [id, stokBaru, hargaBaru]
        item_shops[1] = Baru1 #mengubah ID 2
        for row in item_shops:
            if stokBaru == '':
                print(f"Resilience Potion telah berhasil diubah dengan harga baru {hargaBaru}")
            elif stokBaru == stokBaru:
                print(f"Resilience Potion telah berhasil diubah dengan stok baru sejumlah {stokBaru} dengan harga baru {hargaBaru}")
    elif id == 3:
        Baru2 = [id, stokBaru, hargaBaru]
        item_shops[0] = Baru2 #mengubah ID 1
        for row in item_shops:
            if stokBaru == '':
                print(f"Healing Potion telah berhasil diubah dengan harga baru {hargaBaru}")
            elif stokBaru == stokBaru:
                print(f"Resilience Potion telah berhasil diubah dengan stok baru sejumlah {stokBaru} dengan harga baru {hargaBaru}")

elif (aksi == "hapus") and (hapus == "monster"):
    monsters =  [
["ID","Type","ATK Power","DEF Power","HP","Stok", "Harga"],
[1,"Pikachow",125,10,600,10,500],
[2,"Bulbu",50,50,1200,4,700],
[3,"Zeze",300,10,100,3,300],
[4,"Zuko",100,25,800,8,550],
[5,"Chacha",80,30,700,7,600],
]
    for row in monsters:
        print("|".join(map(str,row)))
    id = int(input("Masukkan id potion: "))

    if id == 1:
            yakin = input("Apakah anda yakin ingin menghapus Pikachow dari shop (y/n): ")
            if yakin == "y" :
                del monsters[0]
                for row in monsters: #menghaspus ID 1
                    print("Pikachow berhasil dihapus dari shop!")

    elif id == 2 :
            yakin = input("Apakah anda yakin ingin menghapus Bulbu dari shop (y/n): ")
            if yakin == "y" :
                del monsters[1]
                for row in monsters:  #menghapus ID 2 
                    print("Bulbu berhasil dihapus dari shop!")           

    elif id == 3 :
            yakin = input("Apakah anda yakin ingin menghapus Zeze dari shop (y/n): ")
            if yakin == "y" :
                del monsters[2]
                for row in monsters: #menghapus ID 3 
                    print("Zeze berhasil dihapus dari shop!")

    elif id == 4 :
            yakin = input("Apakah anda yakin ingin menghapus Zuko dari shop (y/n): ")
            if yakin == "y":
             del monsters[3]
             for row in monsters: #menghapus ID 4 
                print("Zuko berhasil dihapus dari shop!")

    elif id == 5 :
        yakin = input("Apakah anda yakin ingin menghapus Chaca dari shop (y/n): ")
        if yakin == "y" :
           del monsters[4]
           for row in monsters:
                print("Chaca berhasil dihapus dari shop!")

elif (aksi == "hapus") and (hapus == "potion"):
    item_shops = [
["ID", "Type", "Stok", "Harga"],
[1, "Strength Potion", 10, 50],
[2, "Resilience", "Potion", 5, 30],
[3, "Healing Potion", 3, 20],
]
    for row in item_shops:
        print("|".join(map(str,row)) )
    id = int(input("Masukkan id potion: "))

    if id == 1:
        yakin = input("Apakah anda yakin ingin menghapus Strength Potion dari shop (y/n): ")
        if yakin == "y" :
            del item_shops[0]
            for row in item_shops: #menghapus ID 1
                print("Resilience Potion berhasil dihapus dari shop!")

    elif id == 2 :
        yakin = input("Apakah anda yakin ingin menghapus Resilience Potion dari shop (y/n): ")
        if yakin == "y" :
            del item_shops[1]
            for row in item_shops: #menghapus ID 2
               print("Resilience Potion berhasil dihapus dari shop!")           

    elif id == 3 :
        yakin = input("Apakah anda yakin ingin menghapus Healing Potion dari shop (y/n): ")
        if yakin == "y" :
            del item_shops[2]
            for row in item_shops: #menghapus ID 2
                print("Healing Potion berhasil dihapus dari shop!")

elif (aksi == "keluar"):
    print("Dadah {user}, sampai jumpa di lain waktu!")