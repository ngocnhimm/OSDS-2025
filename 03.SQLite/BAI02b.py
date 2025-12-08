import sqlite3
import pandas as pd

DB_FILE = 'Painters_Data_Limited.db'

# 1. Kết nối DB (không xóa, không cào lại)
conn = sqlite3.connect(DB_FILE)

#########################
# A. Thống kê & Toàn cục
#########################

# 1. Đếm tổng số họa sĩ
sql1 = "SELECT COUNT(*) AS total_painters FROM painters_infor;"
df1 = pd.read_sql_query(sql1, conn)
print("1. Tổng số họa sĩ:")
print(df1, "\n")

# 2. Hiển thị 5 dòng đầu
sql2 = "SELECT * FROM painters_infor LIMIT 5;"
df2 = pd.read_sql_query(sql2, conn)
print("2. 5 dòng đầu tiên:")
print(df2, "\n")

# 3. Các quốc tịch duy nhất
sql3 = """
SELECT DISTINCT nationality
FROM painters_infor
WHERE nationality IS NOT NULL AND nationality <> '';
"""
df3 = pd.read_sql_query(sql3, conn)
print("3. Danh sách quốc tịch duy nhất:")
print(df3, "\n")

#########################
# B. Lọc & Tìm kiếm
#########################

# 4. Tên bắt đầu bằng 'F'
sql4 = "SELECT name FROM painters_infor WHERE name LIKE 'F%';"
df4 = pd.read_sql_query(sql4, conn)
print("4. Họa sĩ có tên bắt đầu bằng F:")
print(df4, "\n")

# 5. Quốc tịch chứa 'French'
sql5 = """
SELECT name, nationality
FROM painters_infor
WHERE nationality LIKE '%French%';
"""
df5 = pd.read_sql_query(sql5, conn)
print("5. Họa sĩ có nationality chứa 'French':")
print(df5, "\n")

# 6. Không có quốc tịch
sql6 = """
SELECT name
FROM painters_infor
WHERE nationality IS NULL OR nationality = '';
"""
df6 = pd.read_sql_query(sql6, conn)
print("6. Họa sĩ không có nationality:")
print(df6, "\n")

# 7. Có cả birth và death
sql7 = """
SELECT name
FROM painters_infor
WHERE birth IS NOT NULL AND birth <> ''
  AND death IS NOT NULL AND death <> '';
"""
df7 = pd.read_sql_query(sql7, conn)
print("7. Họa sĩ có đủ ngày sinh & ngày mất:")
print(df7, "\n")

# 8. Tên chứa 'Fales'
sql8 = "SELECT * FROM painters_infor WHERE name LIKE '%Fales%';"
df8 = pd.read_sql_query(sql8, conn)
print("8. Họa sĩ có tên chứa 'Fales':")
print(df8, "\n")

#########################
# C. Nhóm & Sắp xếp
#########################

# 9. Sắp xếp theo tên A–Z
sql9 = "SELECT name FROM painters_infor ORDER BY name ASC;"
df9 = pd.read_sql_query(sql9, conn)
print("9. Tên họa sĩ sắp xếp A–Z:")
print(df9.head(20), "\n")  # in thử 20 dòng đầu cho đỡ dài

# 10. Đếm số họa sĩ theo quốc tịch
sql10 = """
SELECT nationality, COUNT(*) AS painter_count
FROM painters_infor
GROUP BY nationality
ORDER BY painter_count DESC;
"""
df10 = pd.read_sql_query(sql10, conn)
print("10. Số họa sĩ theo từng nationality:")
print(df10, "\n")

# Đóng DB
conn.close()
