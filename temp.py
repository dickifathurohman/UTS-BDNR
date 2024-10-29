import pymongo

# Menghubungkan ke database MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["online_store"]

# Fungsi untuk menambahkan user
def add_user(id_user, nama_lengkap, email, nomor_telepon, alamat):
    user = {
        "_id": id_user,
        "nama_lengkap": nama_lengkap,
        "email": email,
        "nomor_telepon": nomor_telepon,
        "alamat": alamat,
        "Order": [],
        "Keranjang": {
            "harga_keseluruhan": 0,
            "products": []
        },
        "kupon": {}
    }
    db.users.insert_one(user)
    print("User berhasil ditambahkan")

# Fungsi untuk menambahkan produk
def add_product(id_product, nama_produk, deskripsi_produk, kategori, harga, stok, promo):
    product = {
        "_id": id_product,
        "nama_produk": nama_produk,
        "deskripsi_produk": deskripsi_produk,
        "kategori": kategori,
        "harga": harga,
        "stok": stok,
        "promo": promo
    }
    db.products.insert_one(product)
    print("Produk berhasil ditambahkan")

# Fungsi untuk memperbarui stok produk
def update_product_stock(id_product, jumlah):
    db.products.update_one({"_id": id_product}, {"$inc": {"stok": jumlah}})
    print(f"Stok produk {id_product} berhasil diperbarui")

# Fungsi untuk menambahkan pesanan dan memindahkan data dari keranjang ke dalam pesanan
def add_order(id_user, tanggal, status, kode_kupon):
    user = db.users.find_one({"_id": id_user})
    if user and user["Keranjang"]["products"]:
        total_harga = sum([item["total_harga"] for item in user["Keranjang"]["products"]])
        
        # Mengurangi stok produk sesuai dengan jumlah di keranjang
        for item in user["Keranjang"]["products"]:
            product = db.products.find_one({"_id": item["id_product"]})
            if product and product["stok"] >= item["jumlah"]:
                # Update stok produk
                db.products.update_one({"_id": item["id_product"]}, {"$inc": {"stok": -item["jumlah"]}})
            else:
                print(f"Stok tidak cukup untuk produk {item['id_product']}")
                return  # Membatalkan jika ada stok tidak mencukupi

        # Membuat pesanan jika stok mencukupi
        order = {
            "tanggal": tanggal,
            "Status": status,
            "kode_kupon": kode_kupon,
            "harga_keseluruhan": total_harga,
            "products": user["Keranjang"]["products"]
        }
        
        # Menambahkan pesanan dan mengosongkan keranjang
        db.users.update_one({"_id": id_user}, {"$push": {"Order": order}})
        db.users.update_one({"_id": id_user}, {"$set": {"Keranjang.products": [], "Keranjang.harga_keseluruhan": 0}})
        
        print("Order berhasil ditambahkan, stok diperbarui, dan keranjang dikosongkan.")
    else:
        print("Keranjang kosong atau user tidak ditemukan")


# Fungsi untuk memperbarui keranjang (menambah atau mengurangi produk)
def update_cart(id_user, id_product, jumlah):
    product = db.products.find_one({"_id": id_product})
    user = db.users.find_one({"_id": id_user})
    
    if product and user:
        harga_total = product["harga"] * jumlah
        existing_product = next((item for item in user["Keranjang"]["products"] if item["id_product"] == id_product), None)
        
        if existing_product:
            new_quantity = existing_product["jumlah"] + jumlah
            if new_quantity <= 0:
                db.users.update_one({"_id": id_user}, {"$pull": {"Keranjang.products": {"id_product": id_product}}})
            else:
                db.users.update_one({"_id": id_user, "Keranjang.products.id_product": id_product}, {"$set": {"Keranjang.products.$.jumlah": new_quantity, "Keranjang.products.$.total_harga": harga_total}})
        else:
            if jumlah > 0:
                db.users.update_one({"_id": id_user}, {"$push": {"Keranjang.products": {"id_product": id_product, "jumlah": jumlah, "total_harga": harga_total}}})

        updated_cart_total = sum([item["total_harga"] for item in db.users.find_one({"_id": id_user})["Keranjang"]["products"]])
        db.users.update_one({"_id": id_user}, {"$set": {"Keranjang.harga_keseluruhan": updated_cart_total}})
        print("Keranjang berhasil diperbarui")
    else:
        print("Produk atau user tidak ditemukan")
