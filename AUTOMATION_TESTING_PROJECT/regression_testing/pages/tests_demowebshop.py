# demo_login1.py
from selenium.webdriver.common.by import By

def login(driver, email, password):
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Log in']").click()

# test_add_to_cart.py
def test_add_to_cart(driver):
    driver.get("https://demowebshop.tricentis.com/books")
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    assert "The product has been added to your shopping cart" in driver.page_source

# test_complete_purchase_flow.py
def test_complete_purchase_flow(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Books").click()
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    driver.find_element(By.CLASS_NAME, "cart-label").click()
    driver.find_element(By.ID, "termsofservice").click()
    driver.find_element(By.ID, "checkout").click()
    assert "Checkout" in driver.title

# test_crossbrowser.py
def test_browser_title(driver):
    driver.get("https://demowebshop.tricentis.com/")
    assert "Demo Web Shop" in driver.title

# test_footerlink.py
def test_footer_links(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Privacy Notice").click()
    assert "privacy" in driver.current_url

# test_login_validation.py
def test_invalid_login(driver):
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys("invalid@example.com")
    driver.find_element(By.ID, "Password").send_keys("invalidpass")
    driver.find_element(By.XPATH, "//input[@value='Log in']").click()
    assert "Login was unsuccessful" in driver.page_source

# test_logout.py
def test_logout(driver):
    from demo_login1 import login
    login(driver, "valid@example.com", "Password123")
    driver.find_element(By.LINK_TEXT, "Log out").click()
    assert "Log in" in driver.page_source

# test_main_categories.py
def test_all_main_categories(driver):
    categories = ["Books", "Computers", "Electronics", "Apparel & Shoes", "Digital downloads", "Jewelry", "Gift Cards"]
    for category in categories:
        driver.get("https://demowebshop.tricentis.com/")
        driver.find_element(By.LINK_TEXT, category).click()
        assert category.lower().replace(" & ", "-").replace(" ", "-") in driver.current_url

# test_main_category.py
def test_computers_category(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Computers").click()
    assert "computers" in driver.current_url

# test_order_confirmation_page.py
def test_order_confirmation(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Books").click()
    driver.find_element(By.XPATH, "//input[@value='Add to cart']").click()
    driver.find_element(By.CLASS_NAME, "cart-label").click()
    driver.find_element(By.ID, "termsofservice").click()
    driver.find_element(By.ID, "checkout").click()
    assert "Checkout" in driver.title

# test_search_functionality.py
from selenium.webdriver.common.keys import Keys

def test_search(driver):
    driver.get("https://demowebshop.tricentis.com/")
    search_box = driver.find_element(By.ID, "small-searchterms")
    search_box.send_keys("books")
    search_box.send_keys(Keys.ENTER)
    assert "books" in driver.page_source.lower()
