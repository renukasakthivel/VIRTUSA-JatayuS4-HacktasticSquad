from tkinter.tix import Select
import pytest
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def base_url():
    return "https://demowebshop.tricentis.com/"

# ------------------ Utilities ------------------ #
def generate_email():
    return f"testuser_{random.randint(1000,9999)}@example.com"

# ------------------ Parameterized Tests ------------------ #

@pytest.mark.parametrize("first_name,last_name,password", [
    ("Nila", "J", "Nila123"),
    ("John", "Doe", "Password123"),
    ("Priya", "D", "Secure@456")
])
def test_user_registration(driver, base_url, first_name, last_name, password):
    email = generate_email()
    driver.get(base_url + "register")
    driver.find_element(By.ID, "gender-female").click()
    driver.find_element(By.ID, "FirstName").send_keys(first_name)
    driver.find_element(By.ID, "LastName").send_keys(last_name)
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.ID, "ConfirmPassword").send_keys(password)
    driver.find_element(By.ID, "register-button").click()
    assert "Your registration completed" in driver.page_source

@pytest.mark.parametrize("email,password,expected_success", [
    ("srinila@gmail.com", "Nila@123", True),
    ("12345.com", "WrongPass", False),
    ("priya@gmail.com", "_", False)
])
def test_login_parameterized(driver, base_url, email, password, expected_success):
    driver.get(base_url + "login")
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.ID, "RememberMe").click()
    driver.find_element(By.CSS_SELECTOR, "input.login-button").click()
    time.sleep(2)
    if expected_success:
        assert "Log out" in driver.page_source
    else:
        assert "Login was unsuccessful" in driver.page_source

@pytest.mark.parametrize("search_term,expected_result", [
    ("Health Book", True),
    ("laptop", True),
    ("Gift Cards", False)
])
def test_search_functionality(driver, base_url, search_term, expected_result):
    driver.get(base_url)
    search_box = driver.find_element(By.ID, "small-searchterms")
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.submit()
    time.sleep(2)
    if expected_result:
        assert "No products were found" not in driver.page_source
    else:
        assert "No products were found" in driver.page_source

@pytest.mark.parametrize("category_name", [
    "Books",
    "Computers",
    "Electronics",
    "Apparel & Shoes",
    "Digital downloads",
    "Jewelry",
    "Gift Cards"
])
def test_navigation_to_main_categories(driver, base_url, category_name):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, category_name).click()
    WebDriverWait(driver, 10).until(EC.title_contains(category_name))
    assert category_name.lower() in driver.title.lower()

@pytest.mark.parametrize("newsletter_email,is_valid", [
    ("testuser@gmail.com", True),
    ("nilaj08@gmail.com", False) #already registered
])
def test_newsletter_subscription(driver, base_url, newsletter_email, is_valid):
    driver.get(base_url)
    driver.find_element(By.ID, "newsletter-email").send_keys(newsletter_email)
    driver.find_element(By.ID, "newsletter-subscribe-button").click()
    time.sleep(2)
    if is_valid:
        assert "Thank you for signing up!" in driver.page_source
    else:
        assert "Enter valid email" in driver.page_source or "wrong email" in driver.page_source

@pytest.mark.parametrize("product_name", [
    "Health Book",
    "Computing and Internet"
])
def test_add_product_to_cart(driver, base_url, product_name):
    driver.get(base_url)
    search_box = driver.find_element(By.ID, "small-searchterms")
    search_box.clear()
    search_box.send_keys(product_name)
    search_box.submit()
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//h2[@class='product-title']/a[contains(text(),'{product_name}')]"))
    )
    product_link.click()
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "content"))
    )
    assert "The product has been added to your shopping cart" in confirmation.text

# @pytest.mark.parametrize("poll_option_id", [
#     "pollanswers-1",  # Excellent
#     "pollanswers-2"   # Good
# ])
# def test_poll_submission(driver, base_url, poll_option_id):
#     driver.get(base_url)
    
#     # Wait for the poll option to appear and click it
#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.ID, poll_option_id))
#     ).click()

#     # Submit the poll
#     driver.find_element(By.ID, "vote-poll-1").click()

#     # Assertion based on login status
#     assert "Only registered users can vote." in driver.page_source or \
#            "Thank you for voting!" in driver.page_source





