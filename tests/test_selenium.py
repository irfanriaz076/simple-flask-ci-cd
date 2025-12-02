
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = os.environ.get("APP_URL", "http://localhost:5000")

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def test_page_loads_and_has_form():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        input_box = driver.find_element(By.NAME, "name")
        button = driver.find_element(By.TAG_NAME, "button")
        assert input_box is not None
        assert button is not None
    finally:
        driver.quit()

def test_add_user_via_form():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        name_to_add = "E2E_User"

        input_box = driver.find_element(By.NAME, "name")
        button = driver.find_element(By.TAG_NAME, "button")

        input_box.clear()
        input_box.send_keys(name_to_add)
        button.click()

        time.sleep(2)
        lis = driver.find_elements(By.TAG_NAME, "li")
        names = [li.text for li in lis]
        assert name_to_add in names
    finally:
        driver.quit()
