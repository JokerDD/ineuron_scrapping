from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
source_link="https://ineuron.ai/courses"

driver = webdriver.Chrome(executable_path='chromedriverasdasd', options=chrome_options)
driver.get(source_link)
time.sleep(3)
html_source = driver.page_source
print(type(html_source),len(html_source))
