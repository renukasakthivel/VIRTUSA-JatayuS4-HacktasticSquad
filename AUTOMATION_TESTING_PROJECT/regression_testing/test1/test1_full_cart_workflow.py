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
def driver(request):
    driver_path = r"C:\Users\Santhosh J\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"
    options = options()
    options.add_argument("start-maximized")
    driver_instance = webdriver.Chrome(service=ChromeService(driver_path), options=options)
    request.node.driver = driver_instance
    yield driver_instance
    driver_instance.quit()

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

def test_full_cart_workflow(driver):
    wait = WebDriverWait(driver, 10)

    # Step 1: Login
    driver.get("https://demowebshop.tricentis.com/")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()
    wait.until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys("nilaj@gmail.com")
    driver.find_element(By.NAME, "Password").send_keys("Nila123")
    driver.find_element(By.XPATH, "//input[@class='button-1 login-button']").click()

    # Step 2: Search and click Health Book
    search_box = wait.until(EC.presence_of_element_located((By.ID, "small-searchterms")))
    search_box.clear()
    search_box.send_keys("Health Book")
    driver.find_element(By.XPATH, "//input[@value='Search']").click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Health Book"))).click()

    # Step 3: Add to cart
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart']"))).click()

    # Step 4: Go to Cart
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='cart-label']"))).click()

    # Step 5: From cart, click 'Health Book' again
    health_book_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td/a[text()='Health Book']]")))
    health_book_link = health_book_row.find_element(By.XPATH, ".//a[text()='Health Book']")
    health_book_link.click()

    # Step 6: Return to cart again
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='cart-label']"))).click()

   # Step 7: Remove only Health Book
    health_book_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td/a[text()='Health Book']]")))
    remove_checkbox = health_book_row.find_element(By.NAME, "removefromcart")
    remove_checkbox.click()
    driver.find_element(By.NAME, "updatecart").click()

    # Step 8: Estimate shipping
    driver.find_element(By.ID, "CountryId").send_keys("India")
    driver.find_element(By.ID, "ZipPostalCode").send_keys("612504")
    driver.find_element(By.NAME, "estimateshipping").click()


    # Step 9: Agree to terms of service
    wait.until(EC.element_to_be_clickable((By.ID, "termsofservice"))).click()

     # Step 10: Proceed to checkout and confirm checkout page
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.url_contains("checkout"))
    assert "checkout" in driver.current_url