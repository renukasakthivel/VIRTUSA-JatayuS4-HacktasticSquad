import pytest
from selenium import webdriver
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# --------------------------- Fixtures ---------------------------

@pytest.fixture
def driver(request):
    driver_path = r"C:\Users\Santhosh J\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"
    options = ChromeOptions()
    options.add_argument("start-maximized")
    driver_instance = webdriver.Chrome(service=ChromeService(driver_path), options=options)
    request.node.driver = driver_instance
    yield driver_instance
    driver_instance.quit()

@pytest.fixture
def user_credentials():
    return {
        "email": "john.doe@example.com",
        "password": "password"
    }

# Screenshot on failure
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

# --------------------------- Test Cases ---------------------------

def test_user_registration(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.CLASS_NAME, "ico-register").click()
    driver.find_element(By.ID, "gender-male").click()
    driver.find_element(By.ID, "FirstName").send_keys("John")
    driver.find_element(By.ID, "LastName").send_keys("Doe")
    email = f"john.doe{random.randint(1000,9999)}@example.com"
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys("password")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("password")
    driver.find_element(By.ID, "register-button").click()
    assert "Your registration completed" in driver.page_source

def test_product_browsing(driver):
    driver.get("https://demowebshop.tricentis.com/")
    categories = ["Books", "Computers", "Electronics", "Apparel & Shoes", "Digital downloads", "Jewelry", "Gift Cards"]
    for cat in categories:
        driver.find_element(By.LINK_TEXT, cat).click()

def test_search_functionality(driver):
    driver.get("https://demowebshop.tricentis.com/")
    search_box = driver.find_element(By.ID, "small-searchterms")
    search_box.send_keys("books")
    search_box.send_keys(Keys.RETURN)
    assert "books" in driver.page_source.lower()

def test_product_detail_page(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Computers").click()
    driver.find_element(By.LINK_TEXT, "Notebooks").click()
    driver.find_element(By.LINK_TEXT, "14.1-inch Laptop").click()
    driver.find_element(By.ID, "add-to-cart-button-31").click()
    assert "The product has been added to your shopping cart" in driver.page_source

def test_shopping_cart(driver):
    driver.get("https://demowebshop.tricentis.com/cart")
    driver.find_element(By.ID, "updatecartbutton").click()
    assert "Shopping cart" in driver.title

def test_checkout_process(driver, user_credentials):
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys(user_credentials["email"])
    driver.find_element(By.ID, "Password").send_keys(user_credentials["password"])
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()

    driver.find_element(By.LINK_TEXT, "Books").click()
    driver.find_element(By.LINK_TEXT, "Computing and Internet").click()
    driver.find_element(By.ID, "add-to-cart-button-13").click()

    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    driver.find_element(By.ID, "termsofservice").click()
    driver.find_element(By.ID, "checkout").click()

    assert "checkout" in driver.title.lower()

def test_order_history(driver, user_credentials):
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys(user_credentials["email"])
    driver.find_element(By.ID, "Password").send_keys(user_credentials["password"])
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()

    driver.find_element(By.LINK_TEXT, "My account").click()
    driver.find_element(By.LINK_TEXT, "Orders").click()
    assert "order" in driver.page_source.lower()

def test_newsletter_subscription(driver):
    driver.get("https://demowebshop.tricentis.com/")
    email = f"test{random.randint(1000,9999)}@mail.com"
    driver.find_element(By.ID, "newsletter-email").send_keys(email)
    driver.find_element(By.ID, "newsletter-subscribe-button").click()
    page_text = driver.page_source.lower()
    assert "thank you for signing up" in page_text or "email address is already subscribed" in page_text

def test_logout_functionality(driver, user_credentials):
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys(user_credentials["email"])
    driver.find_element(By.ID, "Password").send_keys(user_credentials["password"])
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()
    driver.find_element(By.CLASS_NAME, "ico-logout").click()
    assert "Log in" in driver.page_source

def test_header_and_footer_links(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Contact us").click()
    driver.back()
    driver.find_element(By.LINK_TEXT, "Wishlist").click()
    driver.back()
    driver.find_element(By.LINK_TEXT, "My account").click()
