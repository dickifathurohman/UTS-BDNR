# main.py
from admin_cpy import admin_menu
from login import login_page
import os

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    flag_input_wrong = 0
    while True:
        clear_cmd()
        print("\n[ Aplikasi Online Store ]")
        if flag_input_wrong == 1:
            print("-- Input Tidak Valid --")
        role = input("Masuk sebagai (admin/user) atau ketik 'keluar': ").strip().lower()

        if role == "admin":
            admin_menu()
            flag_input_wrong = 0
        elif role == "user":
            login_page()
            flag_input_wrong = 0
        elif role.lower() == "keluar":
            break
        else:
            flag_input_wrong = 1

if __name__ == "__main__":
    main()
