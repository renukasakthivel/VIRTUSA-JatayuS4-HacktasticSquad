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

def test_complete_purchase_flow(driver):
    driver.get("https://demowebshop.tricentis.com/")

    # Step 1: Login
    driver.find_element(By.LINK_TEXT, "Log in").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys("nilaj08@gmail.com")
    driver.find_element(By.NAME, "Password").send_keys("Nila123")
    driver.find_element(By.NAME, "RememberMe").click()
    driver.find_element(By.XPATH, "//input[@class='button-1 login-button']").click()

    # Step 2: Search Product
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
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
    
    # Open Cart
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Shopping cart"))).click()

    # Proceed to Checkout
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "termsofservice"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # Billing Address Step (Assumes pre-filled address)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Continue']"))).click()

    def fill_billing_address(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_FirstName"))).send_keys("Nila")
        self.driver.find_element(By.ID, "BillingNewAddress_LastName").send_keys("J")
        self.driver.find_element(By.ID, "BillingNewAddress_Email").clear()
        self.driver.find_element(By.ID, "BillingNewAddress_Email").send_keys("nilaj08@gmail.com")
        self.driver.find_element(By.ID, "BillingNewAddress_CountryId").send_keys("India")
        self.driver.find_element(By.ID, "BillingNewAddress_StateProvinceId").send_keys("Other (Non US)")
        self.driver.find_element(By.ID, "BillingNewAddress_City").send_keys("chennai")
        self.driver.find_element(By.ID, "BillingNewAddress_Address1").send_keys("porur")
        self.driver.find_element(By.ID, "BillingNewAddress_ZipPostalCode").send_keys("600116")
        self.driver.find_element(By.ID, "BillingNewAddress_PhoneNumber").send_keys("9876543210")

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='Billing.save()']"))).click()

    def continue_shipping(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='Shipping.save()']"))).click()

    def continue_shipping_method(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='ShippingMethod.save()']"))).click()

    def continue_payment_method(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentMethod.save()']"))).click()

    def continue_payment_info(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentInfo.save()']"))).click()

    def confirm_order(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='ConfirmOrder.save()']"))).click()

    def verify_order_success(self):
        message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Your order has been successfully processed!" in message.text