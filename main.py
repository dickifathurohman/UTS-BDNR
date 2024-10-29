# main.py
from admin import admin_menu
from login import login_page

def main():
    print("-- Aplikasi Online Store --")
    role = input("Masuk sebagai (admin/user): ").strip().lower()

    if role == "admin":
        admin_menu()
    elif role == "user":
        login_page()
    else:
        print("Role tidak valid")

if __name__ == "__main__":
    main()
