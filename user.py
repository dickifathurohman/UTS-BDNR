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

    while True:

        user = users_collection.find_one({"_id": user_id})
        cart = user.get("Keranjang", {})

        if cart and cart.get("products"):
            
            print("\n-- Keranjang Anda --")
            total_harga = cart["harga_keseluruhan"]
            for item in cart["products"]:
                product = products_collection.find_one({"_id": item["id_product"]})
                print(
                    f"{product['_id']} | {product['nama_produk']} | Jumlah: {item['jumlah']} | Total Harga: {item['total_harga']}")

            print(f"Total Harga Keranjang: {total_harga}")

            checkout_choice = input("Checkout keranjang (y/n) atau masukan id produk untuk menghapus: ").lower()
            if checkout_choice == "y":
                checkout(user_id)
                break
            elif checkout_choice == "n":
                break
            else:
                product_to_delete = next((item for item in cart["products"] if item["id_product"] == checkout_choice), None)
                
                if product_to_delete:
                    # Update the total cart price and remove the product
                    total_harga -= product_to_delete["total_harga"]
                    users_collection.update_one(
                        {"_id": user_id},
                        {
                            "$pull": {"Keranjang.products": {"id_product": checkout_choice}},
                            "$set": {"Keranjang.harga_keseluruhan": total_harga}
                        }
                    )
                    print(f"Produk dengan ID {checkout_choice} berhasil dihapus dari keranjang.")

                    db.products.update_one({"_id": checkout_choice}, {"$inc": {"stok": +jumlah}})
                else:
                    print("Input tidak valid.")
        else:
            print("Keranjang Anda kosong.")
            break

def checkout(user_id):
    user = users_collection.find_one({"_id": user_id})
    cart = user.get("Keranjang", {})

    if cart and cart.get("products"):
        total_harga = cart["harga_keseluruhan"]

        user_coupons = user.get("kupon", [])
        if user_coupons:
            print("\n-- Kupon yang Tersedia --")
            for kupon in user_coupons:
                print(
                    f"Kode: {kupon['kode_kupon']} - Nama: {kupon['Nama_kupon']} - Potongan: {kupon['potongan_harga']} - Berlaku hingga: {kupon['valid_until']}")

            coupon_code = input(
                "Masukkan kode kupon atau ketik 'tidak': ").strip()

            # Check if the coupon is in the user's list of available coupons
            valid_coupon = next((kupon for kupon in user.get(
                "kupon", []) if kupon["kode_kupon"] == coupon_code), None)

            if valid_coupon:
                discount = valid_coupon["potongan_harga"]
                total_harga -= discount  # Apply the discount
                print(
                    f"Kupon berhasil digunakan. Potongan sebesar {discount}. Total harga setelah diskon: {total_harga}")
            else:
                coupon_code = None
                print(
                    "Kode kupon tidak valid atau tidak tersedia. Melanjutkan tanpa kupon.")
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


def view_order_history(user_id, order_limit=5):
    pipeline = [
        # Match the user by user_id
        {"$match": {"_id": user_id}},

        # Limit the number of orders
        {"$project": {
            # Limit the number of orders
            "Order": {"$slice": ["$Order", order_limit]},
            "kupon": 1,
            "nama_lengkap": 1,
        }},

        # Unwind the orders to handle each one individually
        {"$unwind": "$Order"},

        # Lookup to join product details for each product in the order
        {
            "$lookup": {
                "from": "products",
                "localField": "Order.products.id_product",
                "foreignField": "_id",
                "as": "Order.products_details"
            }
        },

        # Group the documents back to the original user structure
        {"$group": {
            "_id": "$_id",
            "nama_lengkap": {"$first": "$nama_lengkap"},
            "Order": {"$push": "$Order"},
            "kupon": {"$first": "$kupon"},
        }}
    ]

    # Execute the aggregation pipeline
    result = list(users_collection.aggregate(pipeline))

    if not result:
        print("Anda belum memiliki riwayat order.")
        return

    user = result[0]
    orders = user.get("Order", [])
    coupons = user.get("kupon", [])

    # Print user’s full name
    print(f"Nama Lengkap: {user['nama_lengkap']}\n")

    print("-- Riwayat Order Anda --")
    for order in orders:
        print(f"Tanggal: {order['tanggal']} - Status: {order['Status']}")

        harga_awal = 0
        discount_amount = 0

        # List products in the order with joined details
        for item, product_detail in zip(order["products"], order["products_details"]):
            unit_price = product_detail['harga']
            print(
                f"{product_detail['nama_produk']} - Jumlah: {item['jumlah']}, Harga Satuan: {unit_price}, Total Harga: {item['total_harga']}")
            harga_awal += item['total_harga']

        print(f"\nTotal harga awal: {harga_awal}")

        # Check if a coupon code was applied
        if "kode_kupon" in order:
            coupon_code = order["kode_kupon"]
            # Find the coupon in the user's coupons
            coupon = next(
                (c for c in coupons if c["kode_kupon"] == coupon_code), None)

            if coupon:
                discount_amount = coupon["potongan_harga"]
                print(f"Potongan Harga: {discount_amount} ({coupon_code})")
            else:
                print(f"Potongan Harga: {discount_amount}")

        # Display the total price after applying the discount
        print(f"Total harga Keseluruhan: {order['harga_keseluruhan']}\n")

    print("-" * 30)


def view_products(user_id, limit=3):

    skip = 0

    while True:

        # Fetch products with pagination, sorting by stock, and applying limit
        products = products_collection.find().sort("stok", 1).skip(skip).limit(limit)
        # Convert to a list to check if there are products
        products_list = list(products)

        if not products_list:
            print("Tidak ada produk lagi yang dapat ditampilkan.")
            break

        print("\n-- Daftar Produk --")
        for product in products_list:
            print(f"ID Produk: {product['_id']}")
            print(f"Nama Produk: {product['nama_produk']}")
            print(f"Deskripsi: {product['deskripsi_produk']}")
            print(f"Kategori: {product['kategori']}")
            print(f"Harga: {product['harga']}")
            print(f"Stok: {product['stok']}")
            print("-" * 30)  # Garis pemisah untuk kejelasan

        next_action = input(
            "\nMasukkan ID Produk yang ingin dibeli, lanjut atau selesai untuk mengakhiri: ")

        if next_action.lower() == "lanjut":
            skip += limit
        elif next_action.lower() == "selesai":
            break
        else:
            product = products_collection.find_one({"_id": next_action})

            if product:

                try:
                    jumlah = int(input(
                        "Masukkan jumlah produk yang ingin dibeli (atau ketik '0' untuk membatalkan): "))
                    if jumlah == 0:
                        break
                    if jumlah > product['stok']:
                        print("Jumlah melebihi stok yang tersedia.")
                    else:
                        add_to_cart(user_id, next_action, jumlah, product['harga'])
                        print("Produk berhasil ditambahkan ke keranjang.")
                except ValueError:
                    print("Masukkan jumlah yang valid.")
            else:
                print("ID produk tidak ditemukan / input tidak valid.")


def add_to_cart(user_id, product_id, jumlah, harga_per_item):

    total_harga = jumlah * harga_per_item
    user = users_collection.find_one({"_id": user_id})
    existing_product = next(
        (item for item in user["Keranjang"]["products"] if item["id_product"] == product_id), None)

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
