from datetime import datetime
from connect import db, users_collection, products_collection
from prettytable import PrettyTable
import os
import uuid

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk memotong teks
def truncate_text(text, length):
    if len(text) > length:
        return text[:length] + "..."
    return text

def user_menu(user_id):
    flag_input_wrong = 0
    user = users_collection.find_one({"_id": user_id})

    print("\nSelamat datang,", user["nama_lengkap"])

    while True:
        clear_cmd()
        print("\n-- User Menu --")
        print("1. Lihat Produk")
        print("2. Lihat Keranjang")
        print("3. Lihat Riwayat Order")
        print("4. Logout")

        if flag_input_wrong == 1:
            print("\n-- Pilihan Tidak Valid --")
            choice = input("Pilih opsi: ")
        else:
            choice = input("\nPilih opsi: ")

        if choice.isdigit() and ((int(choice) >= 1) and (int(choice) <= 4)):
            flag_input_wrong = 0

        if choice == "1":
            view_products(user_id)
        elif choice == "2":
            view_cart(user_id)
        elif choice == "3":
            view_order_history(user_id)
        elif choice == "4":
            break
        else:
            flag_input_wrong = 1


def view_cart(user_id):
    flag_input_wrong = 0

    while True:
        clear_cmd()
        user = users_collection.find_one({"_id": user_id})
        cart = user.get("Keranjang", {})

        if cart and cart.get("products"):
            table = PrettyTable()
            table.field_names = ["ID Produk", "Nama Produk", "Jumlah", "Total Harga"]

            total_harga = cart["harga_keseluruhan"]
            for item in cart["products"]:
                product = products_collection.find_one({"_id": item["id_product"]})
                table.add_row([
                    product['_id'],
                    truncate_text(product['nama_produk'], 50),
                    item['jumlah'],
                    f"Rp. {item['total_harga']:,}"
                ])

            print("\n-- Keranjang Anda --")
            print(table)
            print(f"Total Harga Keranjang: Rp. {total_harga:,}")

            if flag_input_wrong == 1:
                print("\n-- Input Tidak Valid --")
                checkout_choice = input("Checkout keranjang (y/n) atau masukan id produk untuk menghapus: ").lower()
            else:
                checkout_choice = input("\nCheckout keranjang (y/n) atau masukan id produk untuk menghapus: ").lower()
            
            if checkout_choice == "y":
                checkout(user_id)
                print("\nPencet [ENTER] untuk kembali...")
                input()
                break
            elif checkout_choice == "n":
                break
            else:
                product_to_delete = next((item for item in cart["products"] if item["id_product"] == checkout_choice), None)
                
                if product_to_delete:
                    flag_input_wrong = 0
                    
                    total_harga -= product_to_delete["total_harga"]
                    users_collection.update_one(
                        {"_id": user_id},
                        {
                            "$pull": {"Keranjang.products": {"id_product": checkout_choice}},
                            "$set": {"Keranjang.harga_keseluruhan": total_harga}
                        }
                    )

                    products_collection.update_one(
                        {"_id": checkout_choice},
                        {"$inc": {"stok": product_to_delete["jumlah"]}}
                    )
                    print(f"Produk dengan ID {checkout_choice} berhasil dihapus dari keranjang.")
                    print("\nPencet [ENTER] untuk kembali...")
                    input()
                else:
                    flag_input_wrong = 1
        else:
            print("-- Keranjang Anda Kosong --")
            print("\nPencet [ENTER] untuk kembali...")
            input()
            break


def checkout(user_id):
    user = users_collection.find_one({"_id": user_id})
    cart = user.get("Keranjang", {})

    if cart and cart.get("products"):
        total_harga = cart["harga_keseluruhan"]

        user_coupons = user.get("kupon", [])
        if user_coupons:
            table = PrettyTable()
            table.field_names = ["Kode", "Nama", "Potongan", "Berlaku Hingga"]

            for kupon in user_coupons:
                table.add_row([
                    kupon['kode_kupon'],
                    kupon['Nama_kupon'],
                    f"Rp. {kupon['potongan_harga']:,}",
                    kupon['valid_until']
                ])

            print("\n-- Kupon yang Tersedia --")
            print(table)

            while True:
                coupon_code = input("Masukkan kode kupon atau ketik 'tidak': ").strip()

                # Cek apakah kode kupon dimiliki
                valid_coupon = next((kupon for kupon in user.get(
                    "kupon", []) if kupon["kode_kupon"] == coupon_code), None)

                if valid_coupon:
                    discount = valid_coupon["potongan_harga"]
                    total_harga -= discount  # mengurangi total harga dengan diskon
                    print(f"\nKupon berhasil digunakan. Potongan sebesar Rp. {discount:,}. Total harga setelah diskon: Rp. {total_harga:,}")
                    break
                elif coupon_code == 'tidak':
                    coupon_code = None
                    print("\n-- Melanjutkan Tanpa Kupon --")
                    break
                else:
                    print("\n-- Kode Kupon Tidak Valid --")
        else:
            coupon_code = None
            print("\nAnda tidak memiliki kupon yang tersedia. Melanjutkan tanpa kupon")

        order = {
            "_id": str(uuid.uuid4()),
            "tanggal": datetime.now().strftime("%Y-%m-%d"),
            "Status": "Diproses",
            "products": cart["products"],
            "harga_keseluruhan": total_harga,
            "kode_kupon": coupon_code  
        }

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


def view_order_history(user_id, order_limit=2):
    clear_cmd()
    current_skip = 0  # skip untuk melewati data

    while True:
        pipeline = [
            {"$match": {"_id": user_id}},

            #Mengurai data order
            {"$unwind": "$Order"},

            # Sorting
            {"$sort": {"Order.tanggal": -1, "Order.Status": 1}},

            {"$group": {
                "_id": "$_id",
                "Order": {"$push": "$Order"},
                "kupon": {"$first": "$kupon"},
                "nama_lengkap": {"$first": "$nama_lengkap"},
                "alamat": {"$first": "$alamat"},
                "telepon": {"$first": "$telepon"}
            }},

            {"$project": {
                "Order": {"$slice": ["$Order", current_skip, order_limit]},
                "kupon": 1,
                "nama_lengkap": 1,
                "alamat": 1,
                "telepon": 1
            }},

            {"$unwind": "$Order"},

            {
                "$lookup": {
                    "from": "products",
                    "localField": "Order.products.id_product",
                    "foreignField": "_id",
                    "as": "Order.products_details"
                }
            },

            {"$group": {
                "_id": "$_id",
                "nama_lengkap": {"$first": "$nama_lengkap"},
                "alamat": {"$first": "$alamat"},
                "telepon": {"$first": "$telepon"},
                "Order": {"$push": "$Order"},
                "kupon": {"$first": "$kupon"}
            }}
        ]

        result = list(users_collection.aggregate(pipeline))

        #periksa apakah ada order atau tidak
        if not result or not result[0].get("Order"):
            print("\n-- Tidak ada riwayat order untuk ditampilkan pada halaman ini --")
            print("Pencet [ENTER] untuk kembali...")
            input()
            return

        user = result[0]
        orders = user.get("Order", [])
        coupons = user.get("kupon", [])

        
        clear_cmd()
        print(f"Nama Lengkap: {user['nama_lengkap']}\n")
        print("-- Riwayat Order Anda --")

        for order in orders:
            harga_awal = 0
            discount_amount = 0

            table = PrettyTable()
            table.field_names = ["Nama Produk", "Jumlah", "Harga Satuan", "Total Harga"]
            
            for item, product_detail in zip(order["products"], order["products_details"]):
                unit_price = product_detail['harga']
                
                table.add_row([
                    truncate_text(product_detail['nama_produk'], 50),
                    item['jumlah'],
                    f"Rp. {unit_price:,}",
                    f"Rp. {item['total_harga']:,}"
                ])

                harga_awal += item['total_harga']
            
            table.align["Nama Produk"] = 'l'
            table.align["Harga Satuan"] = 'l'
            table.align["Total Harga"] = 'l'

            print(f"Tanggal: {order['tanggal']} | Status: {order['Status']}")
            print(table)
            print(f"Total harga awal: Rp. {harga_awal:,}")

            
            if "kode_kupon" in order:
                coupon_code = order["kode_kupon"]
                coupon = next(
                    (c for c in coupons if c["kode_kupon"] == coupon_code), None)

                if coupon:
                    discount_amount = coupon["potongan_harga"]
                    print(f"Potongan Harga: Rp. {discount_amount:,} ({coupon_code})")
                else:
                    print(f"Potongan Harga: Rp. {discount_amount}")

            
            print(f"Total harga Keseluruhan: Rp. {order['harga_keseluruhan']:,}\n")
            print(f"{'-'* 30}\n")

        
        action = input("Ketik 'lanjut' untuk halaman berikutnya, 'sebelum' untuk halaman sebelumnya, atau 'selesai' untuk keluar: ").lower()

        if action == 'lanjut':
            current_skip += order_limit
        elif action == 'sebelum' and current_skip >= order_limit:
            current_skip -= order_limit
        elif action == 'selesai':
            break
        else:
            print("Input tidak valid atau tidak ada data lebih lanjut.")


def view_products(user_id):
    flag_input_wrong = 0

    while True:
        clear_cmd()
        
        products = products_collection.find().sort("stok", 1)
        
        products_list = list(products)

        if not products_list:
            print("Tidak ada produk lagi yang dapat ditampilkan.")
            break

        table = PrettyTable()
        table.field_names = ["ID Produk", "Nama Produk", "Deskripsi", "Kategori", "Harga", "Stok"]

        
        for product in products_list:
            table.add_row([
                product['_id'],
                truncate_text(product['nama_produk'], 50),
                truncate_text(product['deskripsi_produk'], 50),
                product['kategori'],
                f"Rp. {product['harga']:,}",
                product['stok']
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Daftar Produk --")
        print(table)
        if flag_input_wrong == 1:
            pass

        if flag_input_wrong == 1:
            print("\n-- ID produk tidak ditemukan / input tidak valid --")
            next_action = input("Masukkan ID Produk yang ingin dibeli atau selesai untuk mengakhiri: ")
        else:
            next_action = input("\nMasukkan ID Produk yang ingin dibeli atau ketik 'selesai' untuk mengakhiri: ")

        if next_action.lower() == "selesai":
            break
        else:
            product = products_collection.find_one({"_id": next_action})

            if product:
                flag_input_wrong = 0
                
                while True:
                    try:
                        jumlah = int(input("Masukkan jumlah produk yang ingin dibeli (atau ketik '0' untuk membatalkan): "))
                        if jumlah == 0:
                            break
                        if jumlah > product['stok']:
                            print("\n-- Jumlah melebihi stok yang tersedia. --")
                        else:
                            add_to_cart(user_id, next_action, jumlah, product['harga'])
                            print("Produk berhasil ditambahkan ke keranjang.")
                            print("\nPencet [ENTER] untuk melanjutkan...")
                            input()
                            break
                    except ValueError:
                        print("\n-- Masukkan jumlah yang valid. --")

            else:
                flag_input_wrong = 1


def add_to_cart(user_id, product_id, jumlah, harga_per_item):
    total_harga = jumlah * harga_per_item
    user = users_collection.find_one({"_id": user_id})
    existing_product = next(
        (item for item in user["Keranjang"]["products"] if item["id_product"] == product_id), None)

    if existing_product:
        
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
       
        users_collection.update_one(
            {"_id": user_id},
            {
                "$push": {"Keranjang.products": {"id_product": product_id, "jumlah": jumlah, "total_harga": total_harga}},
                "$inc": {"Keranjang.harga_keseluruhan": total_harga}
            }
        )

    db.products.update_one({"_id": product_id}, {"$inc": {"stok": -jumlah}})
