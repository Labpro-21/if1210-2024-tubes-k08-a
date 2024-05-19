
def help(user_role):
        if user_role is None:
            print("=========== HELP ===========")
            print("Kamu belum login sebagai role apapun. Silahkan login terlebih dahulu.")
            print("1. Login: Masuk ke dalam akun yang sudah terdaftar")
            print("2. Register: Membuat akun baru")
            print("")
            print("Footnote:")
            print("1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
            print("2. Jangan lupa untuk memasukkan input yang valid")
        elif user_role == 'Agent':
            print("=========== HELP ===========")
            print(f"Halo Agent {user.name}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:")
            print("1. Logout: Keluar dari akun yang sedang digunakan")
            print("2. Inventory: Melihat owca-dex yang dimiliki oleh Agent")
            print("3. Battle: Untuk melawan monster musuh secara random dan jika menang akan mendapatkan OC (Uang) ")
            print("4. Laboratory: Untuk meingkatkan level dari monster yang kalian punya")
            print("5. Shop: Untuk membeli Monster dan juga potion!! ")
            print("")
            print("Footnote:")
            print("1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
            print("2. Jangan lupa untuk memasukkan input yang valid")
        elif user_role == 'Admin':
            print("=========== HELP ===========")
            print("Selamat datang, Admin. Berikut adalah hal-hal yang dapat kamu lakukan:")
            print("1. Logout: Keluar dari akun yang sedang digunakan")            
            print("2. Shop: Melakukan manajemen pada SHOP sebagai tempat jual beli peralatan Agent")
            print("3. Monster: Melakukan manajemen pada Monster sebagai")
            print("")
            print("Footnote:")
            print("1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
            print("2. Jangan lupa untuk memasukkan input yang valid")

user_database = gamestate_get_user_database(gameState)
user_entry = database_get_entries_at(user_database, user_id)
user_role = user_entry.role
user_name = user_entry.username

help(user_role)