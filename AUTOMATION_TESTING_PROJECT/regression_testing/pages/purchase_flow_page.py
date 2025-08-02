from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PurchaseFlowPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Login Section
    def click_login_link(self):
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()

    def enter_email(self, email):
        self.wait.until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(By.NAME, "Password").send_keys(password)

    def click_remember_me(self):
        self.driver.find_element(By.NAME, "RememberMe").click()

    def click_login_button(self):
        self.driver.find_element(By.XPATH, "//input[@class='button-1 login-button']").click()

    # Search and Add to Cart
    def search_product(self, product_name):
        search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.submit()

    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 add-to-cart-button']"))).click()

    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='cart-label']"))).click()

    def click_checkout(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # Billing and Checkout Process
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
        self.driver.find_element(By.XPATH, "//input[@onclick='Billing.save()']").click()

    def continue_shipping(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='Shipping.save()']"))).click()

    def continue_payment_method(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentMethod.save()']"))).click()

    def continue_payment_info(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentInfo.save()']"))).click()

    def confirm_order(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='ConfirmOrder.save()']"))).click()

    def verify_order_confirmation(self):
        confirmation = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title"))).text
        assert "Your order has been successfully processed!" in confirmation
