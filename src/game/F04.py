
def help(user):
        if user.role is None:
            print("=========== HELP ===========")
            print("Kamu belum login sebagai role apapun. Silahkan login terlebih dahulu.")
            print("1. Login: Masuk ke dalam akun yang sudah terdaftar")
            print("2. Register: Membuat akun baru")
            print("")
            print("Footnote:")
            print("1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
            print("2. Jangan lupa untuk memasukkan input yang valid")
        elif user.role == 'Agent':
            print("=========== HELP ===========")
            print(f"Halo Agent {user.name}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:")
            print("1. Logout: Keluar dari akun yang sedang digunakan")
            print("2. Monster: Melihat owca-dex yang dimiliki oleh Agent")
            print("")
            print("Footnote:")
            print("1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
            print("2. Jangan lupa untuk memasukkan input yang valid")
        elif user.role == 'Admin':
            print("=========== HELP ===========")
            print("Selamat datang, Admin. Berikut adalah hal-hal yang dapat kamu lakukan:")
            print("Logout: Keluar dari akun yang sedang digunakan")            
            print("Shop: Melakukan manajemen pada SHOP sebagai tempat jual beli peralatan Agent")
            print("")
            print("Footnote:")
            print("1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
            print("2. Jangan lupa untuk memasukkan input yang valid")