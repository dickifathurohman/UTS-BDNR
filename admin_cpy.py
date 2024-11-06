from connect import db
from prettytable import PrettyTable
import os

products_collection = db["products"]

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
        print("5. Analysis")
        print("6. Logout")
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
        elif choice == "6":
            break
        else:
            flag_input_wrong = 1


def produk_berdasarkan_penjualan():
    result = db.users.aggregate([
        { '$unwind': '$Order' },
        { '$unwind': '$Order.products' },
        {
            '$group': {
                '_id': '$Order.products.id_product',
                'total_terjual': { '$sum': '$Order.products.jumlah' }
            }
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'produk_info'
            }
        },
        { '$unwind': '$produk_info' },
        {
            '$project': {
                'nama_produk': '$produk_info.nama_produk',
                'total_terjual': 1
            }
        },
        { '$sort': { 'total_terjual': -1 } }
    ])
    
    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Id Produk", "Nama Produk", "Total Terjual"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id'],
                product['nama_produk'],
                product['total_terjual']
            ])

        table.align["Id Produk"] = 'l'
        table.align["Nama Produk"] = 'l'

        print("\n-- Produk yang Paling Banyak Terjual --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def pendapatan_per_produk():
    result = db.users.aggregate([
        { '$unwind': '$Order' },
        { '$unwind': '$Order.products' },
        {
            '$group': {
                '_id': '$Order.products.id_product',
                'total_pendapatan': { '$sum': '$Order.products.total_harga' }
            }
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'produk_info'
            }
        },
        { '$unwind': '$produk_info' },
        {
            '$project': {
                'nama_produk': '$produk_info.nama_produk',
                'total_pendapatan': 1
            }
        },
        { '$sort': { 'total_pendapatan': -1 } }
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Id Produk", "Nama Produk", "Total Pendapatan"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id'],
                product['nama_produk'],
                f"Rp. {product['total_pendapatan']:,}"
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Total Pendapatan dari Setiap Produk --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def penjualan_per_kategori():
    result = db.users.aggregate([
        { '$unwind': '$Order' },
        { '$unwind': '$Order.products' },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'Order.products.id_product',
                'foreignField': '_id',
                'as': 'produk_info'
            }
        },
        { '$unwind': '$produk_info' },
        {
            '$group': {
                '_id': '$produk_info.kategori',
                'total_terjual': { '$sum': '$Order.products.jumlah' }
            }
        },
        { '$sort': { 'total_terjual': -1 } }
    ])
    
    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Kategori Produk", "Total Terjual"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id'],
                product['total_terjual']
            ])

        for column in table.field_names:
                table.align[column] = 'l'

        print("\n-- Jumlah Produk Terjual berdasarkan Kategori --")
        print(table)
    
    print("\nPencet [ENTER] untuk kembali...")
    input()

def pendapatan_per_kategori():
    result = db.users.aggregate([
        { '$unwind': '$Order' },
        { '$unwind': '$Order.products' },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'Order.products.id_product',
                'foreignField': '_id',
                'as': 'produk_info'
            }
        },
        { '$unwind': '$produk_info' },
        {
            '$group': {
                '_id': '$produk_info.kategori',
                'total_pendapatan': { '$sum': '$Order.products.total_harga' },
                'total_terjual': { '$sum': '$Order.products.jumlah' }
            }
        },
        { '$sort': { 'total_pendapatan': -1 } }
    ])
    
    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Kategori Produk", "Total Pendapatan"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id'],
                f"Rp. {product['total_pendapatan']:,}"
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Pendapatan Total Per Kategori --")
        print(table)
    
    print("\nPencet [ENTER] untuk kembali...")
    input()

def pendapatan_per_bulan():
    bulan = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    result = db.users.aggregate([
        { '$unwind': '$Order' },
        {
            '$addFields': {
                'Order.tanggal_date': { '$dateFromString': { 'dateString': '$Order.tanggal' } }
            }
        },
        {
            '$group': {
                '_id': {
                    'tahun': { '$year': '$Order.tanggal_date' },
                    'bulan': { '$month': '$Order.tanggal_date' }
                },
                'total_pendapatan': { '$sum': '$Order.harga_keseluruhan' }
            }
        },
        { '$sort': { '_id.tahun': 1, '_id.bulan': 1 } }
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Tahun", "Bulan", "Total Pendapatan"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id']['tahun'],
                bulan[product['_id']['bulan']],
                f"Rp. {product['total_pendapatan']:,}"
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Total Pendapatan per Bulan --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def penjualan_per_bulan():
    bulan = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    result = db.users.aggregate([
        { '$unwind': '$Order' },
        { '$unwind': '$Order.products' },
        {
            '$addFields': {
                'Order.tanggal_date': { '$dateFromString': { 'dateString': '$Order.tanggal' } }
            }
        },
        {
            '$group': {
                '_id': {
                    'tahun': { '$year': '$Order.tanggal_date' },
                    'bulan': { '$month': '$Order.tanggal_date' }
                },
                'total_terjual': { '$sum': '$Order.products.jumlah' }
            }
        },
        { '$sort': { '_id.tahun': 1, '_id.bulan': 1 } }
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Tahun", "Bulan", "Total Terjual"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id']['tahun'],
                bulan[product['_id']['bulan']],
                product['total_terjual']
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Total Penjualan Per Bulan --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def avg_order_per_bulan():
    bulan = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    result = db.users.aggregate([
        { '$unwind': '$Order' },
        {
            '$group': {
                '_id': {'$month': { '$toDate': "$Order.tanggal" }},
                'rata_rata_nilai_order': { '$avg': "$Order.harga_keseluruhan" }
            }
        },
        { '$sort': { "_id.bulan": 1 } }
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Bulan", "Avg Total Order"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                bulan[product['_id']],
                f"Rp. {product['rata_rata_nilai_order']:,}"
            ])

        table.align["Bulan"] = 'l'
        table.align["Avg Total Order"] = 'l'

        print("\n-- Average Harga Order Per Bulan --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def penjualan_per_bk():
    bulan = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    result = db.users.aggregate([
        { '$unwind': '$Order' },
        {
            '$addFields': {
                'Order.tanggal_date': { '$dateFromString': { 'dateString': '$Order.tanggal' } }
            }
        },
        { 
            '$unwind': '$Order.products' 
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'Order.products.id_product',
                'foreignField': '_id',
                'as': 'produk_info'
            }
        },
        { '$unwind': '$produk_info' },
        {
            '$group': {
                '_id': {
                    'bulan': { '$month': '$Order.tanggal_date' },
                    'kategori': '$produk_info.kategori'
                },
                'total_terjual': { '$sum': '$Order.products.jumlah' }
            }
        },
        { '$sort': { '_id.kategori': 1, '_id.bulan': 1 } }
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Kategori", "Bulan", "Total Terjual"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id']['kategori'],
                bulan[product['_id']['bulan']],
                product['total_terjual']
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Total Penjualan Per Kategori dan Bulan --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def pendapatan_per_bk():
    bulan = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    result = db.users.aggregate([
        { '$unwind': '$Order' },
        {
            '$addFields': {
                'Order.tanggal_date': { '$dateFromString': { 'dateString': '$Order.tanggal' } }
            }
        },
        { 
            '$unwind': '$Order.products' 
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'Order.products.id_product',
                'foreignField': '_id',
                'as': 'produk_info'
            }
        },
        { '$unwind': '$produk_info' },
        {
            '$group': {
                '_id': {
                    'bulan': { '$month': '$Order.tanggal_date' },
                    'kategori': '$produk_info.kategori'
                },
                'total_pendapatan': { '$sum': '$Order.products.total_harga' }
            }
        },
        { '$sort': { '_id.kategori': 1, '_id.bulan': 1 } }
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak ada produk yang terjual...")
    else:
        table = PrettyTable()
        table.field_names = ["Kategori", "Bulan", "Total Pendapatan"]

        # Menambahkan baris ke tabel
        for product in result_list:
            table.add_row([
                product['_id']['kategori'],
                bulan[product['_id']['bulan']],
                f"Rp. {product['total_pendapatan']:,}"
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Total Pendapatan Per Kategori dan Bulan --")
        print(table)

    print("\nPencet [ENTER] untuk kembali...")
    input()

def user_pengeluaran():
    result = db.users.aggregate([
        { '$unwind': '$Order' },
        {
            '$group': {
                '_id': {
                    'email': '$email',
                    'nama_lengkap': '$nama_lengkap'
                },
                'total_pengeluaran': { '$sum': '$Order.harga_keseluruhan' }
            }
        },
        { '$sort': { 'total_pengeluaran': -1 } }
    ])
    
    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak user yang tersedia...")
    else:
        table = PrettyTable()
        table.field_names = ["Nama Lengkap", "Email", "Total Pengeluaran"]

        # Menambahkan baris ke tabel
        for user in result_list:
            table.add_row([
                user['_id']['nama_lengkap'],
                user['_id']['email'],
                f"Rp. {user['total_pengeluaran']:,}"
            ])

        for column in table.field_names:
            table.align[column] = 'l'

        print("\n-- Pengguna yang Paling Banyak Berbelanja --")
        print(table)
    
    print("\nPencet [ENTER] untuk kembali...")
    input()

def user_pemesanan():
    result = db.users.aggregate([
        { '$project': { 'nama_lengkap': 1, 'email': 1, 'total_order': { '$size': "$Order" } } },
        { '$sort': { 'total_order': -1 } }  # Urutkan dari jumlah order tertinggi
    ])

    result_list = list(result)

    if not result_list:
        print("Sayangnya tidak user yang tersedia...")
    else:
        table = PrettyTable()
        table.field_names = ["Nama Lengkap", "Email", "Jumlah Order"]

        # Menambahkan baris ke tabel
        for user in result_list:
            table.add_row([
                user['nama_lengkap'],
                user['email'],
                user['total_order']
            ])

        table.align["Nama Lengkap"] = 'l'
        table.align["Email"] = 'l'

        print("\n-- Pengguna yang Paling Banyak Berbelanja --")
        print(table)
    
    print("\nPencet [ENTER] untuk kembali...")
    input()

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

        print("\nPencet [ENTER] untuk kembali...")
        input()