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
    driver.maximize_window()
    yield driver
    driver.quit()

def test_category_products_navigation(driver):
    driver.get("https://demowebshop.tricentis.com/")

    # Wait for top menu categories
    top_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='top-menu']"))
    )

    # Extract all category links (hrefs and names)
    category_links = top_menu.find_elements(By.XPATH, ".//li/a")
    visited = []

    for index in range(len(category_links)):
        # Re-fetch menu elements after navigation
        top_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='top-menu']"))
        )
        category_links = top_menu.find_elements(By.XPATH, ".//li/a")

        link = category_links[index]
        category_name = link.text.strip()
        if not category_name or category_name in visited:
            continue
        visited.append(category_name)

        print(f"➡️ Clicking category: {category_name}")
        link.click()

        # Wait for products or message
        try:
            product = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='item-box']//h2/a"))
            )
            product_name = product.text
            product.click()

            # Wait for product detail page
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='product-name']/h1"))
            )
            detail_name = driver.find_element(By.XPATH, "//div[@class='product-name']/h1").text
            price = driver.find_element(By.XPATH, "//div[@class='product-price']//span").text
            add_to_cart = driver.find_element(By.XPATH, "//input[@value='Add to cart']")

            print(f"✅ Opened product: {detail_name}, Price: {price}")
            assert product_name in detail_name
            assert add_to_cart.is_displayed()
        except:
            print(f"⚠️ No product found in category: {category_name}")

        driver.back()
        driver.back()  # Go back to homepage to reload menu

