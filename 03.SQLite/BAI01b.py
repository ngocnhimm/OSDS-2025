import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()
# 3. CRUD
# 3.1. Thêm (INSERT)
products_data = [
    ("Laptop A100", 999.99, 15),
    ("Mouse Wireless X", 25.50, 50),
    ("Monitor 27-inch", 249.00, 10)
]

# Lệnh SQL để chèn dữ liệu. Dùng '?' để tráng lỗi SQL Injection
sql2 = """
INSERT INTO products (name, price, quantity) 
VALUES
(?, ?, ?)
"""

# THêm nhiều bản ghi cùng lúc
cursor.executemany(sql2, products_data)
conn.commit() # Lưu thay đổi

# 3.2 READ (SELECT)
sql3 = "SELECT * FROM products"

# Thực thi truy vấn
cursor.execute(sql3)

# Lấy tất cả kết quả
all_products = cursor.fetchall()

# In tiêu đề
print(f"{'ID':<4} | {'Tên Sản Phẩm':<20} | {'Giá':<10} | {'Số Lượng':<10}")

# Lặp và in ra
for p in all_products:
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")

# 3.3 UPDATE
p.execute("UPDATE user SET age = 31 WHERE name = 'Alice'")
conn.commit()


# 3.4 DELETE
p.execute("DELETE FROM user WHERE name  'Bob'")
conn.commit()


