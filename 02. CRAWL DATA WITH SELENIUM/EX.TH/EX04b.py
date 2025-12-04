from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import time

email_input = input("Nhập email/SDT Facebook: ")
password_input = getpass("Nhập mật khẩu Facebook: ")


gecko_path = r"/Users/ngocnhim/osds_repositories/OSDS-2025/02. CRAWL DATA WITH SELENIUM/EX.TH/DOWNLOAD_GGECKO_FIREFOX/geckodriver"
service = Service(gecko_path)
options = webdriver.FirefoxOptions()
options.binary_location ="/Applications/Firefox.app/Contents/MacOS/firefox"
options.headless = False

driver = webdriver.Firefox(service=service, options=options)


driver.get("https://www.facebook.com/login")

email_box = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "email"))
)
email_box.send_keys(email_input)

password_box = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "pass"))
)
password_box.send_keys(password_input)

login_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.NAME, "login"))
)
login_button.click()

time.sleep(500)


post_box = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Bạn đang nghĩ gì?']"))
)
post_box.click()


content = "Hello, đây là bài đăng được tự động tạo bằng Selenium "

text_area = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
)
text_area.send_keys(content)


post_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@aria-label='Đăng' or @aria-label='Post']")
    )
)
post_button.click()

time.sleep(10)
driver.quit()