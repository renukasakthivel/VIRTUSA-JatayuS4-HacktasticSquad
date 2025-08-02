from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
import time

def test_user_registration(driver):
    driver.get("https://demowebshop.tricentis.com/")
    
    # Click Register
    driver.find_element(By.XPATH, "//a[@class='ico-register']").click()
    driver.find_element(By.ID, "gender-male").click()
    driver.find_element(By.ID, "FirstName").send_keys("John")
    driver.find_element(By.ID, "LastName").send_keys("Doe")
    
    # Unique email
    email = f"john{int(time.time())}@example.com"
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys("password123")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("password123")
    driver.find_element(By.ID, "register-button").click()
    
    # Confirm registration success
    assert "Your registration completed" in driver.page_source

# test1_all_categories.py
import pytest
from selenium.webdriver.common.by import By

def test_all_categories_links(driver):
    driver.get("https://demowebshop.tricentis.com/")
    categories = ["Books", "Computers", "Electronics", "Apparel & Shoes", "Digital downloads", "Jewelry", "Gift Cards"]
    for category in categories:
        link = driver.find_element(By.LINK_TEXT, category)
        assert link.is_displayed()


# test1_books_category_filtering.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_books_filtering(driver):
    driver.get("https://demowebshop.tricentis.com/books")
    wait = WebDriverWait(driver, 10)
    filters = ["Under 25.00", "25.00 - 50.00", "Over 50.00"]
    for price in filters:
        xpath = f"//ul[@class='price-range-selector']/li/a[contains(text(),'{price}')]"
        filter_elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        filter_elem.click()
        driver.back()


# test1_categories_products.py
import pytest
from selenium.webdriver.common.by import By

def test_categories_has_products(driver):
    driver.get("https://demowebshop.tricentis.com/")
    categories = ["Books", "Computers", "Electronics"]
    for category in categories:
        driver.find_element(By.LINK_TEXT, category).click()
        assert len(driver.find_elements(By.CLASS_NAME, "product-item")) > 0
        driver.back()


# test1_end_to_end.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def test_end_to_end_register_login_cart_logout(driver):
    driver.get("https://demowebshop.tricentis.com/register")
    driver.find_element(By.ID, "gender-male").click()
    driver.find_element(By.ID, "FirstName").send_keys("Test")
    driver.find_element(By.ID, "LastName").send_keys("User")
    email = f"testuser_{int(time.time())}@mail.com"
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys("Password123")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("Password123")
    driver.find_element(By.ID, "register-button").click()
    driver.get("https://demowebshop.tricentis.com/books")
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    driver.find_element(By.CLASS_NAME, "ico-logout").click()


# test1_footerlink.py
import pytest
from selenium.webdriver.common.by import By

def test_footer_links(driver):
    driver.get("https://demowebshop.tricentis.com/")
    links = ["Sitemap", "Shipping & returns", "Privacy notice", "Conditions of use", "About us", "Contact us"]
    for text in links:
        driver.find_element(By.LINK_TEXT, text).click()
        assert text.lower().replace(" & ", " and ").replace(" ", "-") in driver.current_url
        driver.back()


# test1_full_cart_workflow.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_cart_checkout(driver):
    driver.get("https://demowebshop.tricentis.com/books")
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    driver.find_element(By.CLASS_NAME, "cart-label").click()
    driver.find_element(By.NAME, "updatecart").click()
    assert "shoppingcart" in driver.current_url


# test1_manufacturer_and_newsline.py
import pytest
from selenium.webdriver.common.by import By

def test_manufacturer_and_new_products(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "New products").click()
    assert "newproducts" in driver.current_url
    driver.back()
    driver.find_element(By.LINK_TEXT, "Manufacturers").click()
    assert "manufacturer" in driver.current_url


# test1_top_section.py
import pytest
from selenium.webdriver.common.by import By

def test_top_header_links(driver):
    driver.get("https://demowebshop.tricentis.com/")
    headers = ["Register", "Log in", "Shopping cart", "Wishlist"]
    for item in headers:
        assert driver.find_element(By.LINK_TEXT, item).is_displayed()


# test_computing_and_internet_page_interactivity.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_computing_page_interactions(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://demowebshop.tricentis.com/books")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Computing and Internet"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Email a friend']"))).click()
    assert "productemailafriend" in driver.current_url

