#############################################
# I. IMPORT & KẾT NỐI DATABASE
#############################################
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

#############################################
# I. IMPORT & KẾT NỐI DATABASE
#############################################
import sqlite3
import pandas as pd

db_file = "longchau_db.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

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
sql3 = """
SELECT product_name, price, original_price
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND price_num > original_price_num
"""
df3 = pd.read_sql_query(sql3, conn)
print("Hiển thị")
print(df3)

#4. Kiểm tra định dạng: Liệt kê các unit (đơn vị tính) duy nhất để kiểm tra sự nhất quán trong dữ liệu.
sql4 = """
SELECT DISTINCT unit
FROM sanpham
ORDER BY unit """

df4 = pd.read_sql_query(sql4, conn)
print("Hiển thị")
print(df4)

#5. Tổng số lượng bản ghi: Đếm tổng số sản phẩm đã được cào.
sql5 = """
SELECT COUNT(*) AS total_products 
FROM sanpham
"""
df5 = pd.read_sql_query(sql5, conn)
print("Hiển thị")
print(df5)


#NHÓM 2

#6. Sản phẩm có giảm giá: Hiển thị 10 sản phẩm có mức giá giảm (chênh lệch giữa original_price và price) lớn nhất.
sql6 = """
SELECT
    product_name,
    price,
    original_price,
    original_price_num - price_num AS giam_gia
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND original_price_num > price_num
ORDER BY giam_gia DESC
LIMIT 10 """

df6 = pd.read_sql_query(sql6, conn)
print("Hiển thị")
print(df6)

#7. Sản phẩm đắt nhất: Tìm và hiển thị sản phẩm có giá bán cao nhất.
sql7 = """
SELECT
    product_name,
    price,
    original_price
FROM v_sanpham_num
WHERE price_num = (
    SELECT MAX(price_num)
    FROM v_sanpham_num
) """

df7 = pd.read_sql_query(sql7, conn)
print("Hiển thị")
print(df7)

#8. Thống kê theo đơn vị: Đếm số lượng sản phẩm theo từng Đơn vị tính (unit).
sql8 = """
SELECT
    unit,
    COUNT(*) AS so_san_pham
FROM sanpham
GROUP BY unit
ORDER BY so_san_pham DESC """

df8 = pd.read_sql_query(sql8, conn)
print("Hiển thị")
print(df8)

#9.  Sản phẩm cụ thể: Tìm kiếm và hiển thị tất cả thông tin của các sản phẩm có tên chứa từ khóa "Vitamin C".
sql9 = """
SELECT *
FROM sanpham
WHERE product_name LIKE '%Vitamin C%' """

df9 = pd.read_sql_query(sql9, conn)
print("Hiển thị")
print(df9)

#10. Lọc theo giá: Liệt kê các sản phẩm có giá bán nằm trong khoảng từ 100.000 VNĐ đến 200.000 VNĐ.
sql10 = """
SELECT
    product_name,
    price,
    original_price
FROM v_sanpham_num
WHERE price_num BETWEEN 100000 AND 200000
ORDER BY price_num """

df10 = pd.read_sql_query(sql10, conn)
print("Hiển thị")
print(df10)


#NHÓM 3
# 11. Sắp xếp: Sắp xếp tất cả sản phẩm theo Giá bán từ thấp đến cao
sql11 = """
SELECT
    product_name,
    price,
    original_price
FROM v_sanpham_num
ORDER BY price_num ASC """

df11 = pd.read_sql_query(sql11, conn)
print("Hiển Thị")
print (df11)
    
# 12. Phần trăm giảm giá: Tính phần trăm giảm giá cho mỗi sản phẩm và hiển thị 5 sản phẩm có phần trăm giảm giá cao nhất (Yêu cầu tính toán trong query hoặc sau khi lấy data)
sql12 = """
SELECT
    product_name,
    price,
    original_price,
    ROUND(
        (original_price_num - price_num) * 100.0 / original_price_num,
        2
    ) AS discount_percent
FROM v_sanpham_num
WHERE price_num > 0
  AND original_price_num > 0
  AND original_price_num > price_num
ORDER BY discount_percent DESC
LIMIT 5 """

df12 = pd.read_sql_query(sql12, conn)
print("Hiển Thị")
print (df12)


# 13.Xóa bản ghi trùng lặp: Viết câu lệnh SQL để xóa các bản ghi bị trùng lặp, chỉ giữ lại một bản ghi (sử dụng Subquery hoặc Common Table Expression - CTE).
sql13 = """
DELETE FROM sanpham
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM sanpham
    GROUP BY product_url
)"""

df13 = pd.read_sql_query(sql13, conn)
print("Hiển Thị")
print (df13)

# 14.Phân tích nhóm giá: Đếm số lượng sản phẩm trong từng nhóm giá (ví dụ: dưới 50k, 50k-100k, trên 100k).
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
ORDER BY so_san_pham DESC """

df14 = pd.read_sql_query(sql14, conn)
print("Hiển Thị")
print (df14)

# 15.URL không hợp lệ: Liệt kê các bản ghi mà trường product_url bị NULL hoặc rỗng.
sql15  = """
SELECT *
FROM sanpham
WHERE product_url IS NULL
   OR TRIM(product_url) = '' """

df15 = pd.read_sql_query(sql15, conn)
print("Hiển Thị")
print (df15)
