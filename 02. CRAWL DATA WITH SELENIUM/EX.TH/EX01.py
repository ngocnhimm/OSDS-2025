from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Đường dẫn đến file geckodriver của Nhím trên Mac
gecko_path = "/Users/ngocnhim/osds_repositories/OSDS-2025/02. CRAWL DATA WITH SELENIUM/EX.TH/DOWNLOAD_GGECKO_FIREFOX/geckodriver"

# Khởi tạo Service cho Firefox
ser = Service(gecko_path)

# Tùy chọn cho Firefox
options = Options()

# Muốn set cho chắc thì dùng dòng này:
# options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"

options.headless = False  # Cho hiện giao diện

# Khởi tạo driver Firefox
driver = webdriver.Firefox(options=options, service=ser)

# Tạo url
url = "http://pythonscraping.com/pages/javascript/ajaxDemo.html"

# Truy cập
driver.get(url)

print("Before: ================================\n")
print(driver.page_source)

time.sleep(3)

print("\n\n\n\nAfter: ================================\n")
print(driver.page_source)

driver.quit()
