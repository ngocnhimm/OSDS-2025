#Cào Full Trường Đại Học

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Link cào
url = "https://en.wikipedia.org/wiki/List_of_universities_in_Vietnam"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)


#  Tìm full bảng ở Wiki
tables = driver.find_elements(By.CSS_SELECTOR, "table.wikitable")
print("Số bảng tìm được:", len(tables))

all_rows = []  # list để chứa toàn bộ dòng của tất cả bảng

# Duyệt từng bảng và lấy data
for t_index, table in enumerate(tables):
    print(f"Đang xử lý bảng số {t_index}...")

    # Lấy tất cả các dòng (tr)
    rows = table.find_elements(By.CSS_SELECTOR, "tr")
    if not rows:
        continue

    #  Header
    header_cells = rows[0].find_elements(By.TAG_NAME, "th")
    if not header_cells:
        # một số bảng có thể dùng td làm header
        header_cells = rows[0].find_elements(By.TAG_NAME, "td")

    headers = []
    for idx, cell in enumerate(header_cells):
        col_name = cell.text.strip()
        if col_name == "":
            col_name = f"Col_{idx+1}"
        headers.append(col_name)

    #  Lặp qua các dòng data
    for r in rows[1:]:
        cells = r.find_elements(By.TAG_NAME, "td")
        if not cells:
            continue 

        row_data = {}

        # Gán từng ô vào col
        for idx, cell in enumerate(cells):
            col_name = headers[idx] if idx < len(headers) else f"Extra_{idx+1}"
            text = cell.text.strip()
            row_data[col_name] = text

# Đóng trình duyệt
driver.quit()

df = pd.DataFrame(all_rows)

# Lưu ra file 
df = pd.DataFrame(all_rows)
excel_file = "universities_vietnam.xlsx"

df.to_excel(excel_file, index=False)
