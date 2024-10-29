import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db_onlineshop"]
users_collection = db["users"]
products_collection = db["products"]

def user_menu(user_id):

    user = users_collection.find_one({"_id": user_id})

    print("\nSelamat datang,", user["nama_lengkap"])

    while True:
        print("\n-- User Menu --")
        print("1. Lihat Produk")
        print("2. Lihat Keranjang")
        print("3. Lihat Riwayat Order")
        print("4. Keluar")

        choice = input("Pilih opsi: ")

        if choice == "1":
            view_products(user_id)
        elif choice == "2":
            view_cart(user_id)
        elif choice == "3":
            view_order_history(user_id)
        elif choice == "4":
            print("Terima kasih! Anda telah keluar.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

def view_cart(user_id):
    user = users_collection.find_one({"_id": user_id})
    cart = user.get("Keranjang", {})

    if cart and cart.get("products"):
        print("\n-- Keranjang Anda --")
        total_harga = cart["harga_keseluruhan"]
        for item in cart["products"]:
            product = products_collection.find_one({"_id": item["id_product"]})
            print(f"{product['nama_produk']} - Jumlah: {item['jumlah']}, Total Harga: {item['total_harga']}")

        print(f"Total Harga Keranjang: {total_harga}")
        
        while True:
            checkout_choice = input("Ketik 'checkout' untuk melanjutkan atau 'kembali' untuk ke menu utama: ").lower()
            if checkout_choice == "checkout":
                checkout(user_id)
                break
            elif checkout_choice == "kembali":
                break
            else:
                print("Input tidak valid.")
    else:
        print("Keranjang Anda kosong.")