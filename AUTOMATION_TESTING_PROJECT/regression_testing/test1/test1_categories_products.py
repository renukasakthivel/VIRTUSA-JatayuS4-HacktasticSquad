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

# Fixture to set up the driver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# ✅ Test 1: Home page should load with categories
@pytest.mark.order(1)
def test_homepage_loads(driver):
    driver.get("https://demowebshop.tricentis.com/")
    assert "Demo Web Shop" in driver.title


# ✅ Test 2: Check if all main categories are present
@pytest.mark.order(2)
def test_categories_present(driver):
    driver.get("https://demowebshop.tricentis.com/")
    top_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='top-menu']//a"))
    )
    category_names = [cat.text.strip() for cat in top_menu if cat.text.strip()]
    print(f"✅ Categories found: {category_names}")
    assert "books" in [c.lower() for c in category_names]


# ✅ Test 3: Click on BOOKS category and verify navigation
@pytest.mark.order(3)
def test_books_category_navigation(driver):
    driver.get("https://demowebshop.tricentis.com/")
    
   # Search for 'Health Book'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
    )
    search_box.send_keys("Health Book")
    search_box.submit()

    # Click the product link from search results using XPath
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[@class='product-title']/a[contains(text(),'Health Book')]"))
    )
    product_link.click()

    # Click Add to Cart button on product page using XPath
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart' and contains(@class,'add-to-cart-button')]"))
    )
    add_to_cart_btn.click()

    # Verify confirmation message using XPath
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='content']"))
    )
    assert "The product has been added to your shopping cart" in confirmation.text

    print("✅ Product added to cart successfully via XPath!")


# ✅ Test 4: Select first product in BOOKS and check product detail page
@pytest.mark.order(4)
def test_books_first_product(driver):
    driver.get("https://demowebshop.tricentis.com/books")
    first_product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='product-item']//h2/a"))
    )
    product_name = first_product.text
    first_product.click()

    # Wait for product detail page
    product_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='product-name']/h1"))
    )
    assert product_name in product_heading.text


# ✅ Test 5: Negative Test — Try finding a non-existent category (should fail)
@pytest.mark.order(5)
def test_invalid_category_link(driver):
    driver.get("https://demowebshop.tricentis.com/")
    with pytest.raises(Exception):
        driver.find_element(By.XPATH, "//ul[@class='top-menu']//a[text()='NonExistent']").click()

