#LẤY DATA CỦA 1 DANH MỤC

from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd

# Đường dẫn đến file thực thi geckodriver
gecko_path = "/Users/ngocnhim/osds_repositories/OSDS-2025/02. CRAWL DATA WITH SELENIUM/EX.TH/DOWNLOAD_GGECKO_FIREFOX/geckodriver"

# Khởi tạo đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

#Tạo tuy chọn
options = Options()
options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
#Thiết lập firefox chỉ hiển thị giao diện
options.headless = False

#Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)

url = "https://gochek.vn/collections/micro-thu-am"
driver.get(url)
time.sleep(3)

# Lấy tất cả card sản phẩm
products = driver.find_elements(
    By.CSS_SELECTOR,
    "div.col-md-3.col-sm-4.col-xs-6.pro-loop.col_fix20"
)

print("Số sản phẩm:", len(products))

stt = []
ten = []
gia_moi = []
gia_cu = []
link_sp = []
hinh_anh = []

for i, p in enumerate(products, start=1):

    # Tên + link
    try:
        name_el = p.find_element(By.CSS_SELECTOR, "h3.pro-name a")
        name = name_el.text.strip()
        href = name_el.get_attribute("href")
    except:
        name = ""
        href = ""

    # Giá mới
    try:
        price_new = p.find_element(By.CSS_SELECTOR, "p.pro-price.highlight span:not(.pro-price-del)").text.strip()
    except:
        price_new = ""

    # Giá cũ
    try:
        price_old = p.find_element(By.CSS_SELECTOR, "p.pro-price.highlight span.pro-price-del del.compare-price").text.strip()
    except:
        price_old = ""

    # Ảnh
    try:
        img = p.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    except:
        img = ""

    if name:
        stt.append(i)
        ten.append(name)
        gia_moi.append(price_new)
        gia_cu.append(price_old)
        link_sp.append(href)
        hinh_anh.append(img)

driver.quit()

df = pd.DataFrame({
    "STT": stt,
    "Tên sản phẩm": ten,
    "Giá mới": gia_moi,
    "Giá cũ": gia_cu,
    "Link SP": link_sp,
    "Hình ảnh": hinh_anh
})

df.to_excel("danh_sach_sp_EX02b.xlsx", index=False)
print("Đã lưu gochek_micro.xlsx ra Desktop!")