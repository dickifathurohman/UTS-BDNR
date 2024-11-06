from connect import db, products_collection, users_collection
from prettytable import PrettyTable
import os
from analysis import *

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk memotong teks
def truncate_text(text, length):
    if len(text) > length:
        return text[:length] + "..."
    return text

def admin_menu():
    flag_input_wrong = 0

    while True:
        clear_cmd()
        print("-- Admin Menu --")
        print("1. Tambah Produk")
        print("2. Update Produk")
        print("3. Hapus Produk")
        print("4. Lihat Produk")
        print("5. Lihat Pesanan")
        print("6. Analisis")
        print("7. Logout")
        if flag_input_wrong == 1:
            print("\n-- Pilihan Tidak Valid --")
            choice = input("Pilih opsi: ")
        else:
            choice = input("\nPilih opsi: ")

        if choice.isdigit() and ((int(choice) >= 1) and (int(choice) <= 6)):
            flag_input_wrong = 0

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            view_products()
        elif choice == "5":
            view_user_order()
        elif choice == "6":
            while True:
                clear_cmd()
                print("-- Analysis Based On --")
                print("1. Produk")
                print("2. User")
                print("3. Kembali")
                if flag_input_wrong == 1:
                    print("\n-- Pilihan Tidak Valid --")
                    analysis_based_choice = input("Pilih opsi: ")
                else:
                    analysis_based_choice = input("\nPilih opsi: ")

                if analysis_based_choice.isdigit() and ((int(analysis_based_choice) >= 1) and (int(analysis_based_choice) <= 3)):
                    flag_input_wrong = 0

                if analysis_based_choice == "1":
                    while True:
                        clear_cmd()
                        print("-- Daftar Analysis --")
                        print("1. Penjualan per Produk")
                        print("2. Pendapatan per Produk")
                        print("3. Penjualan per Kategori Produk")
                        print("4. Pendapatan per Kategori Produk")
                        print("5. Penjualan per Bulan")
                        print("6. Pendapatan per Bulan")
                        print("7. Rata-Rata Order Bulanan")
                        print("8. Penjualan per Kategori per Bulan")
                        print("9. Pendapatan per Kategori per Bulan")
                        print("10. Kembali")
                        if flag_input_wrong == 1:
                            print("\n-- Pilihan Tidak Valid --")
                            analysis_option = input("Pilih opsi: ")
                        else:
                            analysis_option = input("\nPilih opsi: ")

                        if analysis_option.isdigit() and ((int(analysis_option) >= 1) and (int(analysis_option) <= 3)):
                            flag_input_wrong = 0

                        if analysis_option == "1":
                            produk_berdasarkan_penjualan()
                        elif analysis_option == "2":
                            pendapatan_per_produk()
                        elif analysis_option == "3":
                            penjualan_per_kategori()
                        elif analysis_option == "4":
                            pendapatan_per_kategori()
                        elif analysis_option == "5":
                            penjualan_per_bulan()
                        elif analysis_option == "6":
                            pendapatan_per_bulan()
                        elif analysis_option == "7":
                            avg_order_per_bulan()
                        elif analysis_option == "8":
                            penjualan_per_bk()
                        elif analysis_option == "9":
                            pendapatan_per_bk()
                        elif analysis_option == "10":
                            break
                        else:
                            flag_input_wrong = 1
                elif analysis_based_choice == "2":
                    while True:
                        clear_cmd()
                        print("-- Daftar Analysis --")
                        print("1. User Berdasarkan Banyak Pengeluaran")
                        print("2. User Berdasarkan Banyak Pemesanan")
                        print("3. Kembali")
                        if flag_input_wrong == 1:
                            print("\n-- Pilihan Tidak Valid --")
                            analysis_option = input("Pilih opsi: ")
                        else:
                            analysis_option = input("\nPilih opsi: ")

                        if analysis_option.isdigit() and ((int(analysis_option) >= 1) and (int(analysis_option) <= 5)):
                            flag_input_wrong = 0

                        if analysis_option == "1":
                            user_pengeluaran()
                        elif analysis_option == "2":
                            user_pemesanan()
                        elif analysis_option == "3":
                            break
                        else:
                            flag_input_wrong = 1
                elif analysis_based_choice == "3":
                    break
                else:
                    flag_input_wrong = 1
        elif choice == "7":
            break
        else:
            flag_input_wrong = 1


def add_product():
    
    _id = input("Masukkan ID produk: ")
    nama_produk = input("Masukkan nama produk: ")
    deskripsi_produk = input("Masukkan deskripsi produk: ")
    kategori = input("Masukkan kategori produk: ")
    harga = int(input("Masukkan harga produk: "))
    stok = int(input("Masukkan stok produk: "))

    product = {
        "_id": _id,
        "nama_produk": nama_produk,
        "deskripsi_produk": deskripsi_produk,
        "kategori": kategori,
        "harga": harga,
        "stok": stok
    }
    products_collection.insert_one(product)
    print("Produk berhasil ditambahkan!")
    print("\nPencet [ENTER] untuk kembali...")
    input()


def update_product():
    
    flag_update_product = 0
    while True:
        if flag_update_product == 1:
            print("\n-- Produk tidak ditemukan! --")

        _id = input("Masukkan ID produk yang ingin di-update atau '0' untuk kembali: ")
        product = products_collection.find_one({"_id": _id})
        if product:

            nama_produk = input("Masukkan nama produk baru: ")
            deskripsi_produk = input("Masukkan deskripsi produk baru: ")
            kategori = input("Masukkan kategori produk baru: ")
            harga = int(input("Masukkan harga produk baru: "))
            stok = int(input("Masukkan stok produk baru: "))

            updated_product = {
                "nama_produk": nama_produk,
                "deskripsi_produk": deskripsi_produk,
                "kategori": kategori,
                "harga": harga,
                "stok": stok
            }

            products_collection.update_one({"_id": _id}, {"$set": updated_product})
            print("Produk berhasil di-update!")
            print("\nPencet [ENTER] untuk kembali...")
            input()
            break
        elif _id == "0":
            break
        else:
            flag_update_product = 1
    

def delete_product():
    
    flag_delete_product = 0
    while True:
        if flag_delete_product == 1:
            print("\n-- Produk tidak ditemukan! --")
        _id = input("Masukkan ID produk yang ingin dihapus atau '0' untuk kembali: ")
        result = products_collection.delete_one({"_id": _id})
        if result.deleted_count > 0:
            print("Produk berhasil dihapus!")
            print("\nPencet [ENTER] untuk kembali...")
            input()
            break
        elif _id == '0':
            break
        else:
            flag_delete_product = 1
        

def view_products():

    while True:
        clear_cmd()

        # Fetch products with pagination, sorting by stock, and applying limit
        products = products_collection.find().sort("stok", 1)
        # Convert to a list to check if there are products
        products_list = list(products)

        if not products_list:
            print("Tidak ada produk lagi yang dapat ditampilkan.")
        else:
            table = PrettyTable()
            table.field_names = ["ID Produk", "Nama Produk", "Deskripsi", "Kategori", "Harga", "Stok"]

            # Menambahkan baris ke tabel
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

            next_action = input(
            "\nKetik selesai untuk kembali atau masukan perintah crud (add/update/delete): ")

            if next_action.lower() == 'selesai':
                break
            elif next_action.lower() == 'add':
                add_product()
            elif next_action.lower() == 'update':
                update_product()
            elif next_action.lower() == 'delete':
                delete_product()
            else:
                print("\nInput tidak valid\n")

def view_user_order():

    while True:
        clear_cmd()

        pipeline = [
            {"$unwind": "$Order"},  # Unwind the Order array to process each order separately
            {
                "$group": {
                    "_id": "$Order.Status",  # Group by order status
                    "count": {"$sum": 1}  # Count the number of orders for each status
                }
            }
        ]

        # Execute the aggregation
        result = users_collection.aggregate(pipeline)

        # Display the order counts by status
        status_counts = {"Diproses": 0, "Dikirim": 0, "Selesai": 0}  # Default values for expected statuses
        for status in result:
            status_name = status["_id"]
            status_counts[status_name] = status["count"]

        print("\n-- Status Order Seluruh User --")
        print(f"1. Total Order Diproses: {status_counts.get('Diproses', 0)}")
        print(f"2. Total Order Dikirim: {status_counts.get('Dikirim', 0)}")
        print(f"3. Total Order Selesai: {status_counts.get('Selesai', 0)}")

        action = input("Pilih angka untuk melihat order berdasarkan status atau 'selesai' untuk kembali: ")
        if action == "1":
            view_all_orders_by_status("Diproses")
        elif action == "2":
            view_all_orders_by_status("Dikirim")
        elif action == "3":
            view_all_orders_by_status("Selesai")
        else:
            break

def view_all_orders_by_status(status):

    clear_cmd()

    pipeline = [
        # Unwind orders to handle each one individually
        {"$unwind": "$Order"},
        {"$sort": {"Order.tanggal": -1}},
        # Match orders based on the provided status
        {"$match": {"Order.Status": status}},
        
        # Lookup to join product details for each product in the order
        {
            "$lookup": {
                "from": "products",
                "localField": "Order.products.id_product",
                "foreignField": "_id",
                "as": "Order.products_details"
            }
        },
        
        # Group documents back to original user structure
        {"$group": {
            "_id": "$_id",
            "nama_lengkap": {"$first": "$nama_lengkap"},
            "email": {"$first": "$email"},
            "alamat": {"$first": "$alamat"},
            "nomor_telepon": {"$first": "$nomor_telepon"},
            "kupon": {"$first": "$kupon"},
            "Order": {"$push": "$Order"}
        }}
    ]

    # Execute the aggregation pipeline
    results = list(users_collection.aggregate(pipeline))

    # Check if there are any matching orders
    if not results:
        print(f"\nTidak ada order dengan status: {status}")
        print("\nPencet [ENTER] untuk kembali...")
        input()
        return

    print(f"\n-- Daftar Order dengan Status: {status} --")
    for user in results:

        alamat = user.get("alamat", {})
        coupons = user.get("kupon", [])

        print(f"\nNama Pengguna: {user['nama_lengkap']}")
        print(f"Alamat: {alamat.get('jalan', '')}, {alamat.get('kota', '')}, {alamat.get('provinsi', '')}, {alamat.get('kode_pos', '')}")
        print(f"No Telepon: {user['nomor_telepon']}")
        
        for order in user["Order"]:
            harga_awal = 0
            discount_amount = 0

            # List products with joined details
            table = PrettyTable()
            table.field_names = ["Nama Produk", "Jumlah", "Harga Satuan", "Total Harga"]
            for item, product_detail in zip(order["products"], order["products_details"]):
                unit_price = product_detail["harga"]

                table.add_row([
                    truncate_text(product_detail['nama_produk'], 50),
                    item['jumlah'],
                    f"Rp. {unit_price:,}",
                    f"Rp. {item['total_harga']:,}"
                ])
                
                harga_awal += item["total_harga"]

            table.align["Nama Produk"] = 'l'
            table.align["Harga Satuan"] = 'l'
            table.align["Total Harga"] = 'l'

            print(f"Id Pemesanan: {order['_id']}")
            print(f"Tanggal: {order['tanggal']} | Status: {order['Status']}")
            print(table)
            print(f"Total harga awal: Rp. {harga_awal:,}")

            # Check if a coupon was applied
            if "kode_kupon" in order:
                coupon_code = order["kode_kupon"]
                coupon = next((c for c in coupons if c["kode_kupon"] == coupon_code), None)

                if coupon:
                    discount_amount = coupon["potongan_harga"]
                    print(f"Potongan Harga: Rp. {discount_amount:,} ({coupon_code})")
                else:
                    print(f"Potongan Harga: Rp. {discount_amount}")

            # Display total price after discount
            print(f"Total harga Keseluruhan: Rp. {order['harga_keseluruhan']}\n")

        print(f"{'-'* 30}\n")

    if status == "Diproses":
        order_id = input("Masukan id_order untuk memverifikasi pengiriman: ")
        update_order_status(user['email'], order_id, "Dikirim")
    elif status == "Dikirim":
        order_id = input("Masukan id_order untuk menyelesaikan pesanan: ")
        update_order_status(user['email'], order_id, "Selesai")
    else:
        print("\nPencet [ENTER] untuk kembali...")
        input()

def update_order_status(user_id, order_id, new_status):
    # Find and update the order status based on user_id and order_id
    result = users_collection.update_one(
        {"email": user_id, "Order._id": order_id},
        {"$set": {"Order.$.Status": new_status}}
    )

    # Check if the update was successful
    if result.matched_count > 0:
        if result.modified_count > 0:
            print(f"Status order dengan ID {order_id} berhasil diubah menjadi '{new_status}'.")
        else:
            print(f"Status order dengan ID {order_id} sudah '{new_status}'.")
    else:
        print("Order tidak ditemukan atau user ID salah.")
    
    print("\nPencet [ENTER] untuk kembali...")
    input()
        