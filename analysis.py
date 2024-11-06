from connect import db
from prettytable import PrettyTable

def truncate_text(text, length):
    if len(text) > length:
        return text[:length] + "..."
    return text

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