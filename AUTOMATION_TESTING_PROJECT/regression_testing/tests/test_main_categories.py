import pytest
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import sleep, time

# Fixture with screenshot and browser support
@pytest.fixture
def driver(request):
    browser = "chrome"
    driver_path = r"E:\Stage3\Testing\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("start-maximized")
        driver_instance = webdriver.Chrome(service=ChromeService(driver_path), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("start-maximized")
        driver_instance = webdriver.Edge(service=EdgeService(driver_path), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1280")
        options.add_argument("--height=800")
        driver_instance = webdriver.Firefox(service=FirefoxService(driver_path), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    request.node.driver = driver_instance
    yield driver_instance
    driver_instance.quit()

# Hook to capture screenshot on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call' and result.failed:
        driver = getattr(item, 'driver', None)
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"{item.name}.png"
            screenshot_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved to: {screenshot_path}")

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_main_categories_using_xpath(driver):
    categories = {
        "Books": "books",
        "Computers": "computers",
        "Electronics": "electronics",
        "Apparel & Shoes": "apparel-shoes",
        "Digital downloads": "digital-downloads",
        "Jewelry": "jewelry",
        "Gift Cards": "gift-cards"
    }

    for category_name, url_slug in categories.items():
        # Use XPath to locate the category link
        xpath = f"//ul[@class='top-menu']//a[normalize-space()='{category_name}']"

        # Re-find the element every time due to page reload
        category_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        category_link.click()

        # Verify that the page loaded correctly
        WebDriverWait(driver, 10).until(EC.url_contains(url_slug))
        assert url_slug in driver.current_url, f"URL missing '{url_slug}' after clicking {category_name}"

        # Optional: verify heading
        heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='page-title']/h1"))
        )
        assert category_name.lower() in heading.text.lower(), f"Heading mismatch for {category_name}"

        print(f"✅ Navigated to: {category_name} ({driver.current_url})")

        # Go back to home for next iteration
        driver.get("https://demowebshop.tricentis.com/")
