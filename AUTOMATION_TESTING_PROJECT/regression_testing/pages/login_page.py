from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        self.driver.find_element(By.ID, "Email").send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(By.ID, "Password").send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, "//input[@value='Log in']").click()
    
