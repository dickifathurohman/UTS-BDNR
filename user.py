from datetime import datetime
from connect import db

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
            checkout_choice = input("Checkout keranjang (y/n) ?: ").lower()
            if checkout_choice == "y":
                checkout(user_id)
                break
            elif checkout_choice == "n":
                break
            else:
                print("Input tidak valid.")
    else:
        print("Keranjang Anda kosong.")

def checkout(user_id):
    user = users_collection.find_one({"_id": user_id})
    cart = user.get("Keranjang", {})

    if cart and cart.get("products"):
        total_harga = cart["harga_keseluruhan"]

        user_coupons = user.get("kupon", [])
        if user_coupons:
            print("\n-- Kupon yang Tersedia --")
            for kupon in user_coupons:
                print(f"Kode: {kupon['kode_kupon']} - Nama: {kupon['Nama_kupon']} - Potongan: {kupon['potongan_harga']} - Berlaku hingga: {kupon['valid_until']}")
            
            coupon_code = input("Masukkan kode kupon atau ketik 'tidak': ").strip()
            
            # Check if the coupon is in the user's list of available coupons
            valid_coupon = next((kupon for kupon in user.get("kupon", []) if kupon["kode_kupon"] == coupon_code), None)
            
            if valid_coupon:
                discount = valid_coupon["potongan_harga"]
                total_harga -= discount  # Apply the discount
                print(f"Kupon berhasil digunakan. Potongan sebesar {discount}. Total harga setelah diskon: {total_harga}")
            else:
                coupon_code = None
                print("Kode kupon tidak valid atau tidak tersedia. Melanjutkan tanpa kupon.")
        else:
            coupon_code = None
            print("\nAnda tidak memiliki kupon yang tersedia. Melanjutkan tanpa kupon")

        order = {
            "tanggal": datetime.now().strftime("%Y-%m-%d"),
            "Status": "Diproses",
            "products": cart["products"],
            "harga_keseluruhan": total_harga,
            "kode_kupon": coupon_code  # Store coupon code if applied
        }

        # Move cart to orders and clear the cart
        users_collection.update_one(
            {"_id": user_id},
            {
                "$push": {"Order": order},
                "$set": {"Keranjang": {"harga_keseluruhan": 0, "products": []}}
            }
        )
        
        print("Checkout berhasil, order Anda telah dibuat.")
    else:
        print("Keranjang kosong, tidak bisa checkout.")

def view_order_history(user_id):
    user = users_collection.find_one({"_id": user_id})

    orders = user.get("Order", [])
    coupons = user.get("kupon", [])

    if orders:
        print("\n-- Riwayat Order Anda --")
        for order in orders:
            print(f"Tanggal: {order['tanggal']} - Status: {order['Status']}")

            
            harga_awal = 0
            discount_amount = 0

            # List products in the order
            for item in order["products"]:
                product = products_collection.find_one({"_id": item["id_product"]})
                print(f"{product['nama_produk']} - Jumlah: {item['jumlah']}, Total Harga: {item['total_harga']}")
                harga_awal += item['total_harga']

            print(f"\nTotal harga awal: {harga_awal}")
            # Check if a coupon code was applied
            if "kode_kupon" in order:
                coupon_code = order["kode_kupon"]
                # Find the coupon in the user's coupons
                coupon = next((c for c in coupons if c["kode_kupon"] == coupon_code), None)

                if coupon:
                    discount_amount = coupon["potongan_harga"]
                    print(f"Potongan Harga: {discount_amount} ({coupon_code})")
                else:
                    print(f"Potongan Harga: {discount_amount}")

            # Display the total price after applying the discount
            print(f"Total harga Keseluruhan: {order['harga_keseluruhan']}\n")
        print("-" * 30) 
    else:
        print("Anda belum memiliki riwayat order.")

def view_products(user_id):

    products = products_collection.find()

    print("\n-- Daftar Produk --")
    for product in products:
        print(f"ID Produk: {product['_id']} | Nama Produk: {product['nama_produk']} | Harga: Harga: {product['harga']}")
    
    while True:

        product_id = input("\nMasukkan ID Produk yang ingin dibeli (atau ketik 'selesai' untuk kembali): ")

        if product_id.lower() == "selesai":
            break
        
        product = products_collection.find_one({"_id": product_id})

        if product:
            print(f"Nama Produk: {product['nama_produk']}")
            print(f"Deskripsi: {product['deskripsi_produk']}")
            print(f"Harga: {product['harga']}")
            print(f"Stok: {product['stok']}")

            try:
                jumlah = int(input("Masukkan jumlah produk yang ingin dibeli (atau ketik '0' untuk membatalkan): "))
                if jumlah == 0:
                    break
                if jumlah > product['stok']:
                    print("Jumlah melebihi stok yang tersedia.")
                else:
                    add_to_cart(user_id, product_id, jumlah, product['harga'])
                    print("Produk berhasil ditambahkan ke keranjang.")
                    break
            except ValueError:
                print("Masukkan jumlah yang valid.")
        else:
            print("ID produk tidak ditemukan.")

def add_to_cart(user_id, product_id, jumlah, harga_per_item):

    total_harga = jumlah * harga_per_item
    user = users_collection.find_one({"_id": user_id})
    existing_product = next((item for item in user["Keranjang"]["products"] if item["id_product"] == product_id), None)
    
    if existing_product:
        # Product already in cart, update quantity and total price
        new_jumlah = existing_product["jumlah"] + jumlah
        new_total_harga = new_jumlah * harga_per_item
        users_collection.update_one(
            {"_id": user_id, "Keranjang.products.id_product": product_id},
            {
                "$set": {
                    "Keranjang.products.$.jumlah": new_jumlah,
                    "Keranjang.products.$.total_harga": new_total_harga
                },
                "$inc": {"Keranjang.harga_keseluruhan": total_harga}
            }
        )
    else:
        # Product not in cart, add it as a new entry
        users_collection.update_one(
            {"_id": user_id},
            {
                "$push": {"Keranjang.products": {"id_product": product_id, "jumlah": jumlah, "total_harga": total_harga}},
                "$inc": {"Keranjang.harga_keseluruhan": total_harga}
            }
        )

    db.products.update_one({"_id": product_id}, {"$inc": {"stok": -jumlah}})