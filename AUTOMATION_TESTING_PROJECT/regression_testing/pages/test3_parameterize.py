#parameterize_main_page_category
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainCategoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_home(self):
        self.driver.get("https://demowebshop.tricentis.com/")

    def click_main_category(self, category_text):
        """
        Clicks on a main category from the top menu using the visible text.
        :param category_text: The visible text of the category (e.g., "Books")
        """
        category_xpath = f"//ul[@class='top-menu']//a[normalize-space(text())='{category_text}']"
        category_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, category_xpath)))
        category_link.click()

    def get_current_url(self):
        return self.driver.current_url

    def get_page_heading(self):
        heading_xpath = "//div[@class='page-title']/h1"
        heading_element = self.wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath)))
        return heading_element.text
    
#test_email_a_friend.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time


# ✅ Fixture to initiate and quit the driver
@pytest.fixture
def driver():
    driver_path = r"C:\path\to\your\chromedriver.exe"  # Change this to your path
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


# ✅ Parametrized test for "Email a Friend"
@pytest.mark.parametrize("friend_email, personal_message", [
    ("validfriend@example.com", "Check out this great book!"),      # ✅ Valid input
    ("invalidemail@", "Invalid email format test"),                 # ❌ Invalid email
    ("", "Empty email field"),                                      # ❌ Blank email
    ("test@example.com", ""),                                       # Valid email, blank message
    ("@@@@@", "@@@###!!! invalid everything")                       # ❌ Special characters
])
def test_email_a_friend_feature(driver, friend_email, personal_message):
    wait = WebDriverWait(driver, 10)

    # Step 1: Open website and register
    driver.get("https://demowebshop.tricentis.com/register")
    wait.until(EC.element_to_be_clickable((By.ID, "gender-male"))).click()
    driver.find_element(By.ID, "FirstName").send_keys("Test")
    driver.find_element(By.ID, "LastName").send_keys("User")
    unique_email = f"test_{int(time.time())}@example.com"
    driver.find_element(By.ID, "Email").send_keys(unique_email)
    driver.find_element(By.ID, "Password").send_keys("TestPass123!")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("TestPass123!")
    driver.find_element(By.ID, "register-button").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result")))

    # Step 2: Navigate to Books -> Computing and Internet
    driver.get("https://demowebshop.tricentis.com/")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Books"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Computing and Internet"))).click()

    # Step 3: Click Email a Friend button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Email a friend']"))).click()

    # Step 4: Fill the form
    wait.until(EC.presence_of_element_located((By.ID, "FriendEmail"))).send_keys(friend_email)
    driver.find_element(By.ID, "PersonalMessage").send_keys(personal_message)
    driver.find_element(By.NAME, "send-email").click()

    # Step 5: Validate result
    if friend_email == "" or "@" not in friend_email:
        assert "Enter friend's email" in driver.page_source or "wrong" in driver.page_source.lower()
    else:
        assert "Your message has been sent" in driver.page_source or "only registered customers" not in driver.page_source

#test_end_to_end_demo_webshop.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver_path = r"C:\path\to\chromedriver.exe"  # 🛠️ Replace with your actual path
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.mark.parametrize("friend_email, personal_message", [
    ("validfriend@example.com", "Check out this book!"),
    ("invalid@", "Invalid email test"),
])
def test_end_to_end_flow(driver, friend_email, personal_message):
    wait = WebDriverWait(driver, 10)
    timestamp = str(int(time.time()))
    email = f"testuser_{timestamp}@mail.com"
    password = "Test12345!"

    # Step 1: Register
    driver.get("https://demowebshop.tricentis.com/register")
    wait.until(EC.element_to_be_clickable((By.ID, "gender-male"))).click()
    driver.find_element(By.ID, "FirstName").send_keys("John")
    driver.find_element(By.ID, "LastName").send_keys("Doe")
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.ID, "ConfirmPassword").send_keys(password)
    driver.find_element(By.ID, "register-button").click()
    assert "Your registration completed" in driver.page_source

    # Step 2: Login
    driver.find_element(By.LINK_TEXT, "Log out").click()
    driver.find_element(By.CLASS_NAME, "ico-login").click()
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()
    assert "Log out" in driver.page_source

    # Step 3: Browse Books > Computing and Internet
    driver.find_element(By.LINK_TEXT, "Books").click()
    driver.find_element(By.LINK_TEXT, "Computing and Internet").click()
    assert "Computing and Internet" in driver.page_source

    # Step 4: Add to Cart
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-qty")))
    assert "1" in driver.find_element(By.CLASS_NAME, "cart-qty").text

    # Step 5: Email a Friend (Parameterized)
    driver.find_element(By.XPATH, "//input[@value='Email a friend']").click()
    driver.find_element(By.ID, "FriendEmail").send_keys(friend_email)
    driver.find_element(By.ID, "PersonalMessage").send_keys(personal_message)
    driver.find_element(By.NAME, "send-email").click()

    if "@" not in friend_email:
        assert "Enter friend's email" in driver.page_source or "wrong" in driver.page_source.lower()
    else:
        assert "Your message has been sent" in driver.page_source

    # Step 6: Newsletter Subscription
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.ID, "newsletter-email").send_keys(email)
    driver.find_element(By.ID, "newsletter-subscribe-button").click()
    assert "Thank you for signing up" in driver.page_source or "already subscribed" in driver.page_source

    # Step 7: Go to Cart & Checkout
    driver.find_element(By.CLASS_NAME, "cart-label").click()
    driver.find_element(By.NAME, "termsofservice").click()
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.presence_of_element_located((By.ID, "billing-buttons-container")))
    driver.find_element(By.XPATH, "//input[@title='Continue']").click()  # Billing
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='Shipping.save()']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='ShippingMethod.save()']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentMethod.save()']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentInfo.save()']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='ConfirmOrder.save()']"))).click()
    assert "Your order has been successfully processed!" in driver.page_source

    # Step 8: Logout
    driver.find_element(By.LINK_TEXT, "Log out").click()
    assert "Log in" in driver.page_source

