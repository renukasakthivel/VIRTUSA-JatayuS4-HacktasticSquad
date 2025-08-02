from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_button_xpath = "//input[@value='Add to cart' and contains(@class,'add-to-cart-button')]"
        self.confirmation_message_xpath = "//p[@class='content']"

    def click_add_to_cart(self):
        """Clicks the 'Add to Cart' button on the product details page."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.add_to_cart_button_xpath))
        ).click()

    def get_confirmation_message(self):
        """Returns the confirmation message text after adding to cart."""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.confirmation_message_xpath))
        )
        return message.text
