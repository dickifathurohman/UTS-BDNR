# login.py
from user import user_menu
from connect import db

users_collection = db["users"]

def login_page():

    print("\n-- Daftar / Masuk --")
    print("1. Daftar Akun Baru")
    print("2. Masuk")

    choice = input("Pilih opsi: ")
    
    if choice == "1":
        register_user()
    elif choice == "2":
        login_user()
    else:
        print("Pilihan tidak valid")

def register_user():

    nama_lengkap = input("Masukkan nama lengkap: ")
    email = input("Masukkan email: ")
    nomor_telepon = input("Masukkan nomor telepon: ")
    jalan = input("Masukkan jalan: ")
    provinsi = input("Masukkan provinsi: ")
    kota = input("Masukkan kota: ")
    kode_pos = input("Masukkan kode pos: ")

    user = {
        "nama_lengkap": nama_lengkap,
        "email": email,
        "nomor_telepon": nomor_telepon,
        "alamat": {
            "jalan": jalan,
            "provinsi": provinsi,
            "kota": kota,
            "kode_pos": kode_pos
        },
        "Order": [],
        "Keranjang": {
            "harga_keseluruhan": 0,
            "products": []
        },
        "kupon": []
    }

    result = users_collection.insert_one(user)
    new_user_id = result.inserted_id
    print("Akun berhasil didaftarkan!")
    user_menu(new_user_id)

def login_user():
    email = input("Masukkan email Anda: ")
    user = users_collection.find_one({"email": email})
    
    if user:
        user_menu(user["_id"])
        #print("Selamat datang,", user["nama_lengkap"])
    else:
        print("Email tidak ditemukan!")
