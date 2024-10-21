from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "iso")
os.makedirs(path, exist_ok=True)

options = webdriver.FirefoxOptions()
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', path)
options.profile = profile
driver = webdriver.Firefox(options=options)

driver.get("https://gofile.io/d/K0RdIL")

time.sleep(3)

download_buttons = driver.find_elements(By.LINK_TEXT, "Download")

for i, button in enumerate(download_buttons):
    try:
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        time.sleep(10)
    except Exception as e:
        print(f"Error processing button {i+1}: {str(e)}")
