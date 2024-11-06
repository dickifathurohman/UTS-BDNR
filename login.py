# login.py
from user_cpy import user_menu
from connect import db
import os

users_collection = db["users"]

def login_page():
    flag_login_page = 0

    print("\n-- Daftar / Masuk --")
    print("1. Daftar Akun Baru")
    print("2. Masuk")

    while True:
        if flag_login_page == 1:
            print("\n-- Pilihan Tidak Valid --")
        choice = input("Pilih opsi: ")
        
        if choice == "1":
            register_user()
            break
        elif choice == "2":
            login_user()
            break
        else:
            flag_login_page = 1

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
    print("\nPencet [ENTER] untuk melanjutkan...")
    input()
    user_menu(new_user_id)

def login_user():
    flag_login_user = 0
    while True:
        if flag_login_user == 1:
            print("\n-- Email Tidak Ditemukan! --")
        email = input("Masukkan email Anda: ")
        user = users_collection.find_one({"email": email})
        
        if user:
            user_menu(user["_id"])
            break
            #print("Selamat datang,", user["nama_lengkap"])
        else:
            flag_login_user = 1
