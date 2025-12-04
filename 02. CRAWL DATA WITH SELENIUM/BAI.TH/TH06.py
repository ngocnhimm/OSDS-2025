#############################################
# I. Lấy tất cả đường dẫn truy cập đến painters
# từ A đến Z (tức 26 ký tự)
#############################################
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
all_links = []

for i in range(97, 123):   # 97 -> 'a', 122 -> 'z'
    try:
        driver = webdriver.Chrome()
        url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
        
        # Mở trang
        driver.get(url)

        # Đợi trang tải
        time.sleep(3)

        # Lấy ra tất cả các thẻ <ul>
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))

        # Chọn thẻ ul thứ 21 (index = 20)
        ul_painters = ul_tags[20]

        # Lấy tất cả thẻ <li> thuộc ul painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Lấy danh sách các url
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]

        for x in links:
            all_links.append(x)

    except:
        print("Error!")

    # Đóng webdriver
    driver.quit()
#############################################
# II. Lấy thông tin của từng họa sĩ
#############################################

count = 0

for link in all_links:
    if count > 3:   # ví dụ lấy thử 4 người đầu
        break
    count += 1

    print(link)

    try:
        # Khởi tạo webdriver
        driver = webdriver.Chrome()

        # Mở trang chi tiết họa sĩ
        url = link
        driver.get(url)

        # Đợi 2 giây
        time.sleep(2)

        # Lấy tên họa sĩ
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lấy ngày sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth)[0]
        except:
            birth = ""

        # Lấy ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
        except:
            death = ""

        # Lấy quốc tịch (BẢN GIÁO TRÌNH)
        try:
            nationality_element = driver.find_element(
                By.XPATH,
                "//th[text()='Nationality']/following-sibling::td"
            )
            nationality = nationality_element.text
        except:
            nationality = ""

        # Tạo dictionary thông tin họa sĩ
        painter = {
            'name': name,
            'birth': birth,
            'death': death,
            'nationality': nationality
        }

        # Đưa vào DataFrame
        painter_df = pd.DataFrame([painter])
        d = pd.concat([d, painter_df], ignore_index=True)

        # Đóng webdriver
        driver.quit()

    except:
        pass

#############################################
# IV. In thông tin + lưu file Excel
#############################################

print(d)

file_name = "danh_sach_sp_TH06.xlsx"
d.to_excel(file_name)

print("DataFrame is written to Excel File successfully.")
