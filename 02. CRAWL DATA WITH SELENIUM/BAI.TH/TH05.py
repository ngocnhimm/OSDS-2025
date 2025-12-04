from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Tạo dataframe rỗng
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

# Khởi tạo webdriver
driver = webdriver.Chrome()

# Mở trang
url = "https://en.wikipedia.org/wiki/Edvard_Munch"
driver.get(url)

# Đợi 2 giây
time.sleep(2)


#### Lấy Data PAGE ( Name, Birth, Death, Nationality)
# Lấy tên họa sĩ
try:
    name = driver.find_element(By.TAG_NAME, "h1").text
except:
    name = ""

# Lấy ngày sinh
try:
    birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
    birth_text = birth_element.text
    birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth_text)[0]   # dùng regex
except:
    birth = ""

# Lấy ngày mất
try:
    death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
    death_text = death_element.text
    death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death_text)[0]
except:
    death = ""

# Lấy quốc tịch
paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")

for p in paragraphs:
    text = p.text.strip()
    # Bước lọc: tìm đoạn có câu "was a ... painter"
    if "was a" in text and "painter" in text:
        print("Đoạn tìm được:\n", text)   # debug cho Nhím xem
        # 2. Regex để bắt quốc tịch
        m = re.search(r"was a\s+([A-Za-z]+)", text)
        if m:
            nationality = m.group(1)      # "Norwegian"
        break

#### Đưa vào Dataframe
# Tạo dictionary chứa thông tin
painter = {
    'name': name,
    'birth': birth,
    'death': death,
    'nationality': nationality
}

# Chuyển dictionary thành DataFrame
painter_df = pd.DataFrame([painter])

# Thêm vào DataFrame chính
d = pd.concat([d, painter_df], ignore_index=True)

# In ra DataFrame
print(d)

# Đóng web driver
driver.quit()

