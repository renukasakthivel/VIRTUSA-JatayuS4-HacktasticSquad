from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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

        # Click Continue after billing
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
        success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Your order has been successfully processed!" in success_message.text
