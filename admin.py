from connect import db
products_collection = db["products"]


def admin_menu():

    while True:
        print("\n-- Admin Menu --")
        print("1. Tambah Produk")
        print("2. Update Produk")
        print("3. Hapus Produk")
        print("4. Lihat Produk")
        print("5. Exit")

        choice = input("Pilih opsi: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            view_products()
        elif choice == "5":
            print("Anda Berhasil keluar dari menu admin.")
            break
        else:
            print("Pilihan tidak valid")


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


def update_product():
    _id = input("Masukkan ID produk yang ingin di-update: ")
    product = products_collection.find_one({"_id": _id})
    if product:

        print(product)

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
    else:
        print("Produk tidak ditemukan!")


def delete_product():
    _id = input("Masukkan ID produk yang ingin dihapus: ")
    result = products_collection.delete_one({"_id": _id})
    if result.deleted_count > 0:
        print("Produk berhasil dihapus!")
    else:
        print("Produk tidak ditemukan!")


def view_products(limit=3):
    skip = 0  # Starting point for pagination

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

        # Ask if the user wants to view the next set of products
        next_action = input(
            "\nKetik 'lanjut' untuk melihat lebih banyak produk, atau 'selesai' untuk kembali: ")

        if next_action.lower() != 'lanjut':
            break

        # Increment skip by the limit to fetch the next set of products in the next loop
        skip += limit
