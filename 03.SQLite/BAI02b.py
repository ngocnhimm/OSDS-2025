import sqlite3
import pandas as pd

DB_FILE = 'Painters_Data_Limited.db'

# 1. Kết nối DB (không xóa, không cào lại)
conn = sqlite3.connect(DB_FILE)

#########################
# A. Thống kê & Toàn cục
#########################

# 1. Đếm tổng số hoạ sĩ
sql1 = "SELECT COUNT (*) AS total_painters FROM painters_infor "
df1 = pd.read_sql_query(sql1, conn)
print("Tổng số hoạ sĩ")
print(df1)

# Hiển thị 5 dòng đầu đi
sql2 = "SELECT * FROM painters_infor LIMIT 5"
df2 = pd.read_sql_query(sql2, conn)
print("Hiển thị 5 dòng đầu data")
print(df2)

#In ra các quốc tịch
sql3 = "SELECT DISTINCT nationality FROM painters_infor WHERE nationality IS NOT NULL AND nationality <> '' "
df3 = pd.read_sql_query(sql3, conn)
print(" In các quốc tịch")
print (df3)

#4. Tìm và hiển thị tên của các họa sĩ có tên bắt đầu bằng ký tự 'F'.
sql4 = "SELECT name FROM painters_infor WHERE name like 'F%' "
df4 = pd.read_sql_query(sql4, conn)
print("Hiển thị tên hoạ sĩ bắt đầu bằng F")
print(df4)

#5. Tìm và hiển thị tên và quốc tịch của những họa sĩ có quốc tịch chứa từ khóa 'French' (ví dụ: French, French-American).
sql5 = "SELECT name, nationality FROM painters_infor WHERE nationality like '%French%' "
df5 = pd.read_sql_query( sql5, conn)
print("Tên và Quốc Tịch của những hoạ sĩ có từ khoá French")
print(df5)

#6. Hiển thị tên của các họa sĩ không có thông tin quốc tịch (hoặc để trống, hoặc NULL).
sql6 = "SELECT name, nationality FROM painters_infor WHERE nationality IS NULL OR nationality = '' "
df6 = pd.read_sql_query(sql6, conn)
print("Hiển thị tên của các hoạ sĩ không có quốc tịch")
print(df6)

#7 7. Tìm và hiển thị tên của những họa sĩ có cả thông tin ngày sinh và ngày mất (không rỗng).
sql7 = "SELECT name, birth, death FROM painters_infor WHERE birth IS NOT NULL AND birth <> ' ' AND death IS NOT NULL AND death <> '' "
df7 = pd.read_sql_query(sql7, conn)
print("Hiển thị tên của những hoạ sĩ có cả thông tin sinh vaf mất")
print(df7)

#8. Hiển thị tất cả thông tin của họa sĩ có tên chứa từ khóa '%Fales%' (ví dụ: George Fales Baker).
sql8 = "SELECT * FROM painters_infor WHERE name like '%Fales%' "
df8 = pd.read_sql_query(sql8, conn)
print("Hiển thị tất cả thông tin của hoạ sĩ chứa tư khoá Fales")
print(df8)

