from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3

# 1. Cấu hình Firefox + geckodriver
gecko_path = "/Users/ngocnhim/osds_repositories/OSDS-2025/02. CRAWL DATA WITH SELENIUM/EX.TH/DOWNLOAD_GGECKO_FIREFOX/geckodriver"


options = webdriver.firefox.options.Options()
options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
options.headless = False  # True nếu muốn chạy ẩn

driver = webdriver.Firefox(service=Service(gecko_path), options=options)

# 2. Mở trang
url = "https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vitamin-khoang-chat"
driver.get(url)
time.sleep(2)

# 3. Bấm nút "Xem thêm" nhiều lần
for _ in range(10):
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(., 'Xem thêm')]")
        btn.click()
        time.sleep(1)
    except:
        break  # không còn nút nữa thì thôi

# 4. Cuộn xuống cho chắc là đã load hết
body = driver.find_element(By.TAG_NAME, "body")
for _ in range(60):
    body.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.02)

time.sleep(2)

# 5. Kết nối SQLite và tạo bảng nếu chưa có
conn = sqlite3.connect("longchau_db.sqlite")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sanpham (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_url TEXT UNIQUE,
    product_name TEXT,
    price TEXT,
    original_price TEXT,
    unit TEXT
)
""")

# 6. Tìm tất cả nút "Chọn mua" (mỗi nút là 1 sản phẩm)
buttons = driver.find_elements(By.XPATH, "//button[text()='Chọn mua']")
print("Tổng sản phẩm tìm được:", len(buttons))

so_sp_luu = 0

# 7. Cào từng sản phẩm
for i, bt in enumerate(buttons, start=1):

    # Lùi lên cha 3 lần để tới card sản phẩm
    card = bt
    for _ in range(3):
        card = card.find_element(By.XPATH, "./..")

    # Tên sản phẩm
    try:
        name = card.find_element(By.TAG_NAME, "h3").text
    except:
        name = ""

    # Giá bán
    try:
        price = card.find_element(By.CLASS_NAME, "text-blue-5").text
    except:
        price = ""

    # Giá gốc (nếu không có thì = giá bán)
    try:
        original_price = card.find_element(By.CLASS_NAME, "line-through").text
    except:
        original_price = price

    # Link chi tiết sản phẩm
    try:
        link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = ""

    if link == "" or name == "":
        continue  # thiếu info cơ bản thì bỏ qua

    # Lấy đơn vị (unit) từ trang chi tiết
    unit = "Không rõ"
    try:
        # mở tab mới
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        try:
            # cố lấy phần 'Quy cách'
            unit = driver.find_element(
                By.XPATH,
                "//div[contains(@class,'label') and contains(.,'Quy cách')]/following-sibling::div[1]"
            ).text
        except:
            unit = "Không rõ"
    finally:
        # đóng tab chi tiết, quay về tab chính
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # Lưu vào DB
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO sanpham (product_url, product_name, price, original_price, unit)
            VALUES (?, ?, ?, ?, ?)
        """, (link, name, price, original_price, unit))

        if cursor.rowcount > 0:
            so_sp_luu += 1
    except Exception as e:
        print("Lỗi khi lưu:", e)

# 8. Lưu thay đổi + đóng mọi thứ
conn.commit()
conn.close()
driver.quit()

print("Số sản phẩm lưu được vào DB:", so_sp_luu)
