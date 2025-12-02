import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# The app URL is provided by Jenkins / environment; default for local dev:
BASE_URL = os.environ.get("APP_URL", "http://localhost:5000")

# Path to ChromeDriver installed on your EC2 (from your earlier steps)
CHROMEDRIVER_PATH = "/usr/bin/chromedriver/chromedriver"


def get_driver():
    """
    Create a headless Chrome WebDriver instance using the system ChromeDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def test_page_loads_and_has_form():
    """
    Test case 1:
    - Page loads successfully
    - Input and button elements exist
    """
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
    """
    Test case 2:
    - Submit a user name via form
    - Verify it appears in the user list
    """
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
