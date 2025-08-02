from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DemoWebShopPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 1. Registration with missing fields
    def go_to_registration_page(self):
        self.driver.get("https://demowebshop.tricentis.com/register")

    def submit_blank_registration(self):
        self.driver.find_element(By.ID, "register-button").click()

    def get_registration_error(self):
        return self.driver.find_element(By.ID, "FirstName-error").text

    # 2. Login with wrong credentials
    def go_to_login_page(self):
        self.driver.get("https://demowebshop.tricentis.com/login")

    def login_with_invalid_credentials(self, email, password):
        self.driver.find_element(By.ID, "Email").send_keys(email)
        self.driver.find_element(By.ID, "Password").send_keys(password)
        self.driver.find_element(By.XPATH, "//input[@value='Log in']").click()

    def get_login_error(self):
        return self.driver.find_element(By.XPATH, "//div[@class='message-error validation-summary-errors']").text

    # 3. Search with blank input
    def submit_blank_search(self):
        self.driver.find_element(By.ID, "small-searchterms").clear()
        self.driver.find_element(By.XPATH, "//input[@value='Search']").click()

    def get_search_error(self):
        return self.driver.find_element(By.XPATH, "//div[@class='no-result']").text

    # 4. Add to cart without selecting attributes
    def go_to_product_page(self):
        self.driver.get("https://demowebshop.tricentis.com/build-your-own-computer")

    def add_to_cart_without_attributes(self):
        self.driver.find_element(By.ID, "add-to-cart-button-1").click()

    def get_cart_error(self):
        return self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='message-error']"))).text

    # 5. Email a friend without being logged in
    def go_to_any_product(self):
        self.driver.get("https://demowebshop.tricentis.com/14-inch-laptop")

    def click_email_a_friend(self):
        self.driver.find_element(By.XPATH, "//input[@value='Email a friend']").click()

    def get_email_friend_error(self):
        return self.driver.find_element(By.XPATH, "//div[@class='message-error']").text
