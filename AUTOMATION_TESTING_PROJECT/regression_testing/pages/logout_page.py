from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_logout(self):
        logout_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log out")))
        logout_link.click()

    def is_logged_out(self):
        return "Log in" in self.driver.page_source
