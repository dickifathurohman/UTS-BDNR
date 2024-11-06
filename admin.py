from connect import db
products_collection = db["products"]
users_collection = db["users"]

def admin_menu():

    while True:
        print("\n-- Admin Menu --")
        print("1. Tambah Produk")
        print("2. Update Produk")
        print("3. Hapus Produk")
        print("4. Lihat Produk")
        print("5. Lihat Pesanan User")
        print("6. Exit")

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
            view_user_orders()
        elif choice == "6":
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

        if next_action.lower() == 'lanjut':
            # Increment skip by the limit to fetch the next set of products in the next loop
            skip += limit
        elif next_action.lower() == 'add':
            add_product()
        elif next_action.lower() == 'update':
            update_product()
        elif next_action.lower() == 'delete':
            delete_product()
        else:
            break

def view_user_orders():

    while True:
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
    pipeline = [
        # Unwind orders to handle each one individually
        {"$unwind": "$Order"},
        
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
        return

    print(f"\n-- Daftar Order dengan Status: {status} --")
    for user in results:

        alamat = user.get("alamat", {})

        print(f"\nNama Pengguna: {user['nama_lengkap']}")
        print(f"Alamat: {alamat.get('jalan', '')}, {alamat.get('kota', '')}, {alamat.get('provinsi', '')}, {alamat.get('kode_pos', '')}")
        print(f"No Telepon: {user['nomor_telepon']}")
        
        # Get the user's coupons if any
        coupons = user.get("kupon", [])
        
        for order in user["Order"]:
            print(f"Tanggal: {order['tanggal']} - Status: {order['Status']}\n")
            total_initial_price = 0
            discount_amount = 0

            # List products with joined details
            print("-- Produk dipesan --")
            for item, product_detail in zip(order["products"], order["products_details"]):
                unit_price = product_detail["harga"]
                print(f"{product_detail['nama_produk']} - Jumlah: {item['jumlah']}, Harga Satuan: {unit_price}, Total Harga: {item['total_harga']}")
                total_initial_price += item["total_harga"]

            print(f"\nTotal Harga Awal: {total_initial_price}")

            # Check if a coupon was applied
            if "kode_kupon" in order:
                coupon_code = order["kode_kupon"]
                coupon = next((c for c in coupons if c["kode_kupon"] == coupon_code), None)

                if coupon:
                    discount_amount = coupon["potongan_harga"]
                    print(f"Potongan Harga: {discount_amount} ({coupon_code})")
                else:
                    print("Potongan Harga: 0")

            # Display total price after discount
            print(f"Total Harga Keseluruhan: {order['harga_keseluruhan']}\n")

        print("-" * 30)


