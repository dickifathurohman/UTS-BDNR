import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#create database
mydb = myclient['db_onlineshop']

product_collection = mydb['products']

# Sample data for 20 products
products = [
    {
        "_id": "prod001",
        "nama_produk": "Happy Tos Keripik Tortilla Merah 140g",
        "deskripsi_produk": "Keripik renyah nan lezat yang terbuat dari biji jagung pilihan.",
        "kategori": "Makanan Ringan",
        "harga": 12000,
        "stok": 50
    },
    {
        "_id": "prod002",
        "nama_produk": "Fitbar Snack Bar Fruits Delight 20g",
        "deskripsi_produk": "Snack sehat rasa kismis yang terbuat dari berbagai bahan alami.",
        "kategori": "Makanan Ringan",
        "harga": 6000,
        "stok": 200
    },
    {
        "_id": "prod003",
        "nama_produk": "MamyPoko Popok Celana Bayi L 28pcs",
        "deskripsi_produk": "Popok celana slim agar si kecil nyaman bergerak, dengan ban pinggan yang lembut.",
        "kategori": "Kebutuhan Ibu & Anak",
        "harga": 50000,
        "stok": 30
    },
    {
        "_id": "prod004",
        "nama_produk": "Hydro Coco Minuman Air Kelapa Original 500ml",
        "deskripsi_produk": "Minuman isotonik alami dari Kalibe yang berbeda dari minuman isotonik lainnya.",
        "kategori": "Minuman",
        "harga": 12000,
        "stok": 100
    },
    {
        "_id": "prod005",
        "nama_produk": "Posh Men Body Spray Pria Cool Blue 150ml",
        "deskripsi_produk": "Parfum pria yang dikemas modern dalam bentuk spray yang praktis.",
        "kategori": "Personal Care",
        "harga": 20000,
        "stok": 60
    },
    {
        "_id": "prod006",
        "nama_produk": "Azarine Hydramax C Sunscreen",
        "deskripsi_produk": "Tabir surya untuk wajah dengan tekstur gel.",
        "kategori": "Personal Care",
        "harga": 45000,
        "stok": 120
    },
    {
        "_id": "prod007",
        "nama_produk": "Bebelac Gold 3 Susu Bubuk Vanilla 700g",
        "deskripsi_produk": "Susu tinggi serat, dilengkapi dengan fish oil.",
        "kategori": "Kebutuhan Ibu & Anak",
        "harga": 110000,
        "stok": 25
    }
]

# Insert product documents into the collection
result = product_collection.insert_many(products)
print(f"Inserted {len(result.inserted_ids)} product documents.")

#create collection
user_collection = mydb['users']
# Sample data for 20 users
documents = [
    {
        "nama_lengkap": "John Doe",
        "email": "john.doe@example.com",
        "nomor_telepon": "123-456-7890",
        "alamat": {
            "jalan": "123 Main St",
            "provinsi": "California",
            "kota": "Los Angeles",
            "kode_pos": "90001"
        },
        "Order": [
            {
                "tanggal": "2024-10-01",
                "Status": "Selesai",
                "products": [
                    {"id_product": "prod001", "jumlah": 2, "total_harga": 24000},   # Happy Tos Keripik Tortilla Merah 140g
                    {"id_product": "prod002", "jumlah": 1, "total_harga": 6000}     # Fitbar Snack Bar Fruits Delight 20g
                ],
                "kode_kupon": "DISCOUNT5",
                "harga_keseluruhan": 25000  # harga keseluruhan setelah penyesuaian
            }
        ],
        "Keranjang": {
            "products": [
                {"id_product": "prod003", "jumlah": 3, "total_harga": 150000}     # MamyPoko Popok Celana Bayi L 28pcs
            ],
            "harga_keseluruhan": 150000  # harga keseluruhan setelah penyesuaian
        },
        "kupon": [{
            "kode_kupon": "DISCOUNT5",
            "Nama_kupon": "Discount 5ribu",
            "valid_until": "2024-12-31",
            "potongan_harga": 5000
        }]
    },
    {
        "nama_lengkap": "Jane Smith",
        "email": "jane.smith@example.com",
        "nomor_telepon": "987-654-3210",
        "alamat": {
            "jalan": "456 Elm St",
            "provinsi": "Texas",
            "kota": "Dallas",
            "kode_pos": "75001"
        },
        "Order": [
            {
                "tanggal": "2024-09-15",
                "Status": "Selesai",
                "products": [
                    {"id_product": "prod004", "jumlah": 2, "total_harga": 24000},   # Hydro Coco Minuman Air Kelapa Original 500ml
                    {"id_product": "prod005", "jumlah": 1, "total_harga": 20000}    # Posh Men Body Spray Pria Cool Blue 150ml
                ],
                "kode_kupon": None,
                "harga_keseluruhan": 44000,  # harga keseluruhan setelah penyesuaian
            }
        ],
        "Keranjang": {
            "products": [
                {"id_product": "prod006", "jumlah": 4, "total_harga": 180000}     # Azarine Hydramax C Sunscreen
            ],
            "harga_keseluruhan": 180000,  # harga keseluruhan setelah penyesuaian
        },
        "kupon": [{
            "kode_kupon": "SAVE20",
            "Nama_kupon": "Save 20ribu",
            "valid_until": "2025-01-01",
            "potongan_harga": 20000
        }]
    }
]

# Insert documents into the collection
result = user_collection.insert_many(documents)
print(f"Inserted {len(result.inserted_ids)} documents.")