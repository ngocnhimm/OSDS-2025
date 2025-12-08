#############################################
# I. IMPORT & KẾT NỐI DATABASE
#############################################
import sqlite3
import pandas as pd

db_file = "longchau_db.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

#############################################
# II. VIEW PHỤ: CHUYỂN GIÁ TEXT → SỐ
#############################################
# Bảng sanpham đang lưu price/original_price dạng text (vd: '150.000đ')
# Tạo view v_sanpham_num có thêm 2 cột:
#   - price_num
#   - original_price_num
# để dễ lọc, so sánh, tính giảm giá
sql_view = """
CREATE VIEW IF NOT EXISTS v_sanpham_num AS
SELECT
    product_id,
    product_url,
    product_name,
    price,
    original_price,
    unit,
    CAST(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(price, '.', ''),
                '₫', ''),
            'đ', ''),
        ' ', '')
        AS INTEGER
    ) AS price_num,
    CAST(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(original_price, '.', ''),
                '₫', ''),
            'đ', ''),
        ' ', '')
        AS INTEGER
    ) AS original_price_num
FROM sanpham
"""
cursor.execute(sql_view)
conn.commit()

print("Đã tạo/kiểm tra view v_sanpham_num xong.\n")

#############################################
# III. NHÓM 1 – KIỂM TRA CHẤT LƯỢNG DỮ LIỆU
#############################################

# 1. Duplicate: trùng product_url HOẶC product_name
sql1 = """
SELECT *
FROM sanpham
WHERE product_url IN (
    SELECT product_url
    FROM sanpham
    WHERE product_url IS NOT NULL AND TRIM(product_url) <> ''
    GROUP BY product_url
    HAVING COUNT(*) > 1
)
OR product_name IN (
    SELECT product_name
    FROM sanpham
    WHERE product_name IS NOT NULL AND TRIM(product_name) <> ''
    GROUP BY product_name
    HAVING COUNT(*) > 1
)
"""
df1 = pd.read_sql_query(sql1, conn)
print("1. Bản ghi trùng (theo URL hoặc tên):", len(df1))
print(df1.head(5), "\n")

# 2. Sản phẩm thiếu giá bán (price NULL / rỗng / = 0)
sql2 = """
SELECT COUNT(*) AS missing_price_count
FROM sanpham
WHERE price IS NULL
   OR TRIM(price) = ''
   OR REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(price, '.', ''),
            '₫', ''),
        'đ', ''),
    ' ', '') = '0'
"""
df2 = pd.read_sql_query(sql2, conn)
print("2. Số sản phẩm thiếu giá bán:", df2["missing_price_count"][0], "\n")

# 3. Giá bán > Giá gốc (logic bất thường)
sql3 = """
SELECT product_name, price, original_price
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND price_num > original_price_num
"""
df3 = pd.read_sql_query(sql3, conn)
print("3. Sản phẩm có price > original_price:", len(df3))
print(df3.head(5), "\n")

# 4. Liệt kê unit (đơn vị tính) duy nhất
sql4 = """
SELECT DISTINCT unit
FROM sanpham
ORDER BY unit
"""
df4 = pd.read_sql_query(sql4, conn)
print("4. Các đơn vị unit khác nhau:", len(df4))
print(df4, "\n")

# 5. Tổng số lượng bản ghi
sql5 = """
SELECT COUNT(*) AS total_products
FROM sanpham
"""
df5 = pd.read_sql_query(sql5, conn)
print("5. Tổng số sản phẩm đã cào:", df5["total_products"][0], "\n")

#############################################
# IV. NHÓM 2 – KHẢO SÁT & PHÂN TÍCH
#############################################

# 6. Top 10 sản phẩm giảm giá nhiều nhất (theo số tiền)
sql6 = """
SELECT product_name, price, original_price,
       original_price_num - price_num AS giam_gia
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND original_price_num > price_num
ORDER BY giam_gia DESC
LIMIT 10
"""
df6 = pd.read_sql_query(sql6, conn)
print("6. Top 10 sản phẩm giảm giá nhiều nhất:")
print(df6, "\n")

# 7. Sản phẩm đắt nhất (giá bán cao nhất)
sql7 = """
SELECT product_name, price, original_price
FROM v_sanpham_num
WHERE price_num = (
    SELECT MAX(price_num) FROM v_sanpham_num
)
"""
df7 = pd.read_sql_query(sql7, conn)
print("7. Sản phẩm có giá bán cao nhất:")
print(df7, "\n")

# 8. Thống kê số sản phẩm theo đơn vị unit
sql8 = """
SELECT unit, COUNT(*) AS so_san_pham
FROM sanpham
GROUP BY unit
ORDER BY so_san_pham DESC
"""
df8 = pd.read_sql_query(sql8, conn)
print("8. Số sản phẩm theo từng unit:")
print(df8, "\n")

# 9. Tìm sản phẩm tên chứa 'Vitamin C'
sql9 = """
SELECT *
FROM sanpham
WHERE product_name LIKE '%Vitamin C%'
"""
df9 = pd.read_sql_query(sql9, conn)
print("9. Sản phẩm có tên chứa 'Vitamin C':", len(df9))
print(df9.head(10), "\n")

# 10. Sản phẩm có giá từ 100k đến 200k
sql10 = """
SELECT product_name, price
FROM v_sanpham_num
WHERE price_num BETWEEN 100000 AND 200000
ORDER BY price_num
"""
df10 = pd.read_sql_query(sql10, conn)
print("10. Sản phẩm giá từ 100k–200k:", len(df10))
print(df10.head(10), "\n")

#############################################
# V. NHÓM 3 – TRUY VẤN NÂNG CAO
#############################################

# 11. Sắp xếp tất cả sản phẩm theo giá bán tăng dần
sql11 = """
SELECT product_name, price, original_price
FROM v_sanpham_num
ORDER BY price_num ASC
"""
df11 = pd.read_sql_query(sql11, conn)
print("11. Tổng sản phẩm (sắp xếp theo giá tăng dần):", len(df11))
print(df11.head(10), "\n")

# 12. Top 5 sản phẩm có % giảm giá cao nhất
sql12 = """
SELECT product_name, price, original_price,
       ROUND(
           (original_price_num - price_num) * 100.0 / original_price_num,
           2
       ) AS discount_percent
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND original_price_num > price_num
ORDER BY discount_percent DESC
LIMIT 5
"""
df12 = pd.read_sql_query(sql12, conn)
print("12. Top 5 sản phẩm có % giảm giá cao nhất:")
print(df12, "\n")

# 13. Câu lệnh XÓA bản ghi trùng (giữ lại 1 bản ghi theo product_url)
# !!! CẨN THẬN: LỆNH NÀY SẼ XÓA DỮ LIỆU. NHỚ BACKUP TRƯỚC KHI CHẠY !!!
sql13 = """
DELETE FROM sanpham
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM sanpham
    GROUP BY product_url
)
"""
# Nếu muốn thật sự xóa trùng lặp, bỏ comment 2 dòng dưới:
# cursor.execute(sql13)
# conn.commit()
print("13. Đã chuẩn bị câu lệnh xóa bản ghi trùng (chưa chạy mặc định).\n")

# 14. Phân tích nhóm giá: dưới 50k, 50k–100k, trên 100k
sql14 = """
SELECT
    CASE
        WHEN price_num < 50000 THEN 'Dưới 50k'
        WHEN price_num BETWEEN 50000 AND 100000 THEN '50k-100k'
        ELSE 'Trên 100k'
    END AS nhom_gia,
    COUNT(*) AS so_san_pham
FROM v_sanpham_num
WHERE price_num > 0
GROUP BY nhom_gia
ORDER BY so_san_pham DESC
"""
df14 = pd.read_sql_query(sql14, conn)
print("14. Phân tích số sản phẩm theo nhóm giá:")
print(df14, "\n")

# 15. URL không hợp lệ (NULL hoặc rỗng)
sql15 = """
SELECT *
FROM sanpham
WHERE product_url IS NULL
   OR TRIM(product_url) = ''
"""
df15 = pd.read_sql_query(sql15, conn)
print("15. Sản phẩm có URL không hợp lệ:", len(df15))
print(df15.head(10), "\n")

#############################################
# VI. ĐÓNG KẾT NỐI
#############################################
conn.close()
print("Đã đóng kết nối DB.")
