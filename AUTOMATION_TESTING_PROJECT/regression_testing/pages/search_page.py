from selenium.webdriver.common.by import By

class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_search_text(self, text):
        self.driver.find_element(By.ID, "small-searchterms").send_keys(text)

    def click_search_button(self):
        self.driver.find_element(By.XPATH, "//input[@value='Search']").click()
