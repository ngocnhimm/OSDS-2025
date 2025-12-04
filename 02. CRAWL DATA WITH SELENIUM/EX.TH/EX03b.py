from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import getpass  


username_cli = input("Nhập username: ")
password_cli = getpass.getpass("Nhập password: ")


# Đường dẫn đến file thực thi geckodriver
gecko_path = r"/Users/ngocnhim/osds_repositories/OSDS-2025/02. CRAWL DATA WITH SELENIUM/EX.TH/DOWNLOAD_GGECKO_FIREFOX/geckodriver"


# Khởi tạo đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options();
options.binary_location ="/Applications/Firefox.app/Contents/MacOS/firefox"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

driver = webdriver.Firefox(options=options, service=ser)
wait = WebDriverWait(driver, 15)


url = "https://sso.hutech.edu.vn/login-sso?client_id=7c2075d1-9539-4061-b32b-ca9873f13e13&backlink=https:%2F%2Fhocvudientu.hutech.edu.vn&redirect=%2Fdang-nhap%3FReturnUrl%3D%2F"
driver.get(url)

print("URL ban đầu:", driver.current_url)


username_input = wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Tài khoản của bạn']")
    )
)
username_input.clear()
username_input.send_keys(username_cli)

password_input = wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Mật khẩu của bạn']")
    )
)
password_input.clear()
password_input.send_keys(password_cli)

time.sleep(1)


password_input.send_keys(Keys.RETURN)
time.sleep(5)

if "sso.hutech.edu.vn/login-sso" in driver.current_url:
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        )

time.sleep(10)
driver.quit()
