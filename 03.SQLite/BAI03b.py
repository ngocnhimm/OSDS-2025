import sqlite3
import pandas as pd

db_file = "longchau_db.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
#NHÓM 1
#1. Kiểm tra trùng lặp (Duplicate Check): Kiểm tra và hiển thị tất cả các bản ghi có sự trùng lặp dựa trên trường product_url hoặc product_name.
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
) """
df1 = pd.read_sql_query(sql1, conn)
print("Hiển thị")
print(df1)

#2. Kiểm tra dữ liệu thiếu (Missing Data): Đếm số lượng sản phẩm không có thông tin Giá bán (price là NULL hoặc 0).
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
    ' ', '') = '0' """
df2 = pd.read_sql_query(sql2, conn)
print("Hiển thị")
print(df2)

#3.  Kiểm tra giá: Tìm và hiển thị các sản phẩm có Giá bán lớn hơn Giá gốc/Giá niêm yết (logic bất thường).
sqlite3 = """"
SELECT product_name, price, original_price
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND price_num > original_price_num
"""


