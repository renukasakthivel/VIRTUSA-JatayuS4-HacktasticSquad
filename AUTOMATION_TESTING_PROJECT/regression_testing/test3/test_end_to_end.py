import time
import pytest
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from selenium.common.exceptions import TimeoutException

# Fixture with screenshot and browser support
@pytest.fixture
def driver(request):
    browser = "chrome"
    driver_path = r"E:\Stage3\Testing\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("start-maximized")
        driver_instance = webdriver.Chrome(service=ChromeService(driver_path), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("start-maximized")
        driver_instance = webdriver.Edge(service=EdgeService(driver_path), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1280")
        options.add_argument("--height=800")
        driver_instance = webdriver.Firefox(service=FirefoxService(driver_path), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    request.node.driver = driver_instance
    yield driver_instance
    driver_instance.quit()

# Hook to capture screenshot on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call' and result.failed:
        driver = getattr(item, 'driver', None)
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"{item.name}.png"
            screenshot_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved to: {screenshot_path}")

#Register with user details
def generate_email():
    return f"john{random.randint(1000,9999)}@example.com"

@pytest.fixture(scope="module")
def user_credentials():
    return {
        "first_name": "Nila",
        "last_name": "J",
        "email": generate_email(),
        "password": "Nila123"
    }

def test_user_registration(driver, user_credentials):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.CLASS_NAME, "ico-register").click()
    driver.find_element(By.ID, "gender-male").click()
    driver.find_element(By.ID, "FirstName").send_keys(user_credentials["first_name"])
    driver.find_element(By.ID, "LastName").send_keys(user_credentials["last_name"])
    driver.find_element(By.ID, "Email").send_keys(user_credentials["email"])
    driver.find_element(By.ID, "Password").send_keys(user_credentials["password"])
    driver.find_element(By.ID, "ConfirmPassword").send_keys(user_credentials["password"])
    driver.find_element(By.ID, "register-button").click()
    assert "Your registration completed" in driver.page_source

#Login with user details
def test_positive_login(driver):
    driver.get("https://demowebshop.tricentis.com/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']"))).send_keys("srinila@gmail.com")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Password']"))).send_keys("Nila@123")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='RememberMe']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button' or @value='Log in']"))).click()

    logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Log out']")))
    assert logout.is_displayed()

#Invalid username Login
def test_invalid_username_login(driver):
    driver.get("https://demowebshop.tricentis.com/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']"))).send_keys("invalid_username")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Password']"))).send_keys("Nila@123")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='RememberMe']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button' or @value='Log in']"))).click()

    error = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-error')]")))
    assert error.is_displayed()

#Invalid password Login
def test_invalid_password_login(driver):
    driver.get("https://demowebshop.tricentis.com/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']"))).send_keys("srinila@gmail.com")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Password']"))).send_keys("invalid_password")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='RememberMe']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button' or @value='Log in']"))).click()

    error = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-error')]")))
    assert error.is_displayed()

#Login with empty fields
def test_empty_fields_login(driver):
    driver.get("https://demowebshop.tricentis.com/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']"))).send_keys("")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Password']"))).send_keys("")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='RememberMe']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button' or @value='Log in']"))).click()

    error = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-error')]")))
    assert error.is_displayed()

#Product Browsing
def test_product_browsing(driver):
    driver.get("https://demowebshop.tricentis.com/")
    categories = ["Books", "Computers", "Electronics", "Apparel & Shoes", "Digital downloads", "Jewelry", "Gift Cards"]
    for cat in categories:
        driver.find_element(By.LINK_TEXT, cat).click()

#Search Functionality
def test_search_functionality(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.ID, "small-searchterms").send_keys("books")
    driver.find_element(By.ID, "small-searchterms").send_keys(Keys.RETURN)
    assert "book" in driver.page_source.lower()

#Top Section
def pause(seconds=1.5):
    time.sleep(seconds)

def test_top_section(driver):
    driver.get("https://demowebshop.tricentis.com/")
    pause()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()
    pause()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys("nilaj@gmail.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password"))).send_keys("Nila123")
    pause()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "RememberMe"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button']"))).click()
    pause()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Tricentis Demo Web Shop']")))
    driver.find_element(By.XPATH, "//img[@alt='Tricentis Demo Web Shop']").click()
    pause()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='account' and contains(text(),'nilaj@gmail.com')]")))
    pause()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ico-wishlist']"))).click()
    WebDriverWait(driver, 10).until(EC.title_contains("Wishlist"))
    pause()
    driver.back()
    pause()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ico-cart']"))).click()
    WebDriverWait(driver, 10).until(EC.title_contains("Shopping Cart"))
    pause()
    driver.back()
    pause()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ico-logout']"))).click()
    pause()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Register")))

    assert driver.current_url == "https://demowebshop.tricentis.com/"

    def test_manufacturers_and_newsletter_sections(driver):
     driver.get("https://demowebshop.tricentis.com/")

    # Click on the "Tricentis" link under the "Manufacturers" section
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='block block-manufacturer-navigation']//a[contains(text(),'Tricentis')]"))
    ).click()

    # Verify the manufacturer URL
    assert driver.current_url == "https://demowebshop.tricentis.com/tricentis"

    # Subscribe to newsletter
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='NewsletterEmail']"))
    ).send_keys("nila08@gmail.com")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Subscribe']"))
    ).click()

#Logout Functionality
def test_logout_functionality(driver, user_credentials):
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys(user_credentials["email"])
    driver.find_element(By.ID, "Password").send_keys(user_credentials["password"])
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()
    driver.find_element(By.LINK_TEXT, "Log out").click()
    assert "Register" in driver.page_source
    
#checkout 
def test_add_product_to_cart_xpath(driver):
    driver.get("https://demowebshop.tricentis.com/")

     # Wait for the login link to be clickable
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()
    except TimeoutException:
        print("Login link not found")

    # Enter username and password
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email")))
    username_input.send_keys("nilaj08@gmail.com")
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))
    password_input.send_keys("Nila123")

    # Submit the login form
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "RememberMe"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button']"))).click()


    # Search for 'Health Book'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
    )
    search_box.send_keys("Health Book")
    search_box.submit()

    # Click the product link from search results using XPath
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[@class='product-title']/a[contains(text(),'Health Book')]"))
    )
    product_link.click()

    # Click Add to Cart button on product page using XPath
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart' and contains(@class,'add-to-cart-button')]"))
    )
    add_to_cart_btn.click()

    # Verify confirmation message using XPath
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='content']"))
    )
    assert "The product has been added to your shopping cart" in confirmation.text
    
    # Open Cart
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Shopping cart"))).click()

    # Proceed to Checkout
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "termsofservice"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

#Header and Footer Links
def test_header_and_footer_links(driver):
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.LINK_TEXT, "Contact us").click()
    driver.back()
    driver.find_element(By.LINK_TEXT, "Wishlist").click()
    driver.back()
    driver.find_element(By.LINK_TEXT, "My account").click()

def test_footer_links_sequential_click():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/")
    driver.maximize_window()

    footer_xpath = "//div[@class='footer']//ul//li/a"

    # Wait until footer links are present
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, footer_xpath))
    )

    # Get all footer links except "Follow us" section (based on visible text)
    all_links = driver.find_elements(By.XPATH, footer_xpath)
    footer_links = [link for link in all_links if "facebook" not in link.get_attribute("href").lower()
                    and "twitter" not in link.get_attribute("href").lower()
                    and "rss" not in link.get_attribute("href").lower()
                    and "youtube" not in link.get_attribute("href").lower()
                    and "google" not in link.get_attribute("href").lower()]

    total_links = len(footer_links)

    for index in range(total_links):
        # Re-locate all footer links fresh each time
        footer_links = driver.find_elements(By.XPATH, footer_xpath)
        valid_links = [link for link in footer_links if "facebook" not in link.get_attribute("href").lower()
                       and "twitter" not in link.get_attribute("href").lower()
                       and "rss" not in link.get_attribute("href").lower()
                       and "youtube" not in link.get_attribute("href").lower()
                       and "google" not in link.get_attribute("href").lower()]
        
        link = valid_links[index]
        href = link.get_attribute("href")
        text = link.text.strip()

        print(f"🟢 Clicking on: {text} => {href}")
        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        link.click()

        # Wait for the new page to load + wait 1 second
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print(f"✅ Visited: {driver.current_url} -> Going back")
        driver.back()

        # Wait for homepage to reload before next link
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, footer_xpath))
        )

    driver.quit()

#add product to cart
def test_add_product_to_cart_xpath(driver):
    driver.get("https://demowebshop.tricentis.com/")

     # Wait for the login link to be clickable
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()
    except TimeoutException:
        print("Login link not found")

    # Enter username and password
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email")))
    username_input.send_keys("nilaj08@gmail.com")
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))
    password_input.send_keys("Nila123")

    # Submit the login form
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "RememberMe"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button-1 login-button']"))).click()


    # Search for 'Health Book'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
    )
    search_box.send_keys("Health Book")
    search_box.submit()

    # Click the product link from search results using XPath
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[@class='product-title']/a[contains(text(),'Health Book')]"))
    )
    product_link.click()

    # Click Add to Cart button on product page using XPath
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart' and contains(@class,'add-to-cart-button')]"))
    )
    add_to_cart_btn.click()

    # Verify confirmation message using XPath
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='content']"))
    )
    assert "The product has been added to your shopping cart" in confirmation.text
    
    # Open Cart
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Shopping cart"))).click()

    # Proceed to Checkout
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "termsofservice"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # Billing Address Step (Assumes pre-filled address)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Continue']"))).click()

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
        message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Your order has been successfully processed!" in message.text
    
    # ✅ MAIN TEST FUNCTION
def test_computing_and_internet_page_interactivity(driver):
    wait = WebDriverWait(driver, 10)

    # Step 1: Open homepage
    driver.get("https://demowebshop.tricentis.com/")

    # Step 1: Register a new user
    driver.get("https://demowebshop.tricentis.com/register")
    wait.until(EC.element_to_be_clickable((By.ID, "gender-male"))).click()
    driver.find_element(By.ID, "FirstName").send_keys("Test")
    driver.find_element(By.ID, "LastName").send_keys("User")

    import time
    unique_email = f"testuser_{int(time.time())}@mail.com"
    driver.find_element(By.ID, "Email").send_keys(unique_email)
    driver.find_element(By.ID, "Password").send_keys("Password123!")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("Password123!")
    driver.find_element(By.ID, "register-button").click()

    # Confirm registration
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result")))
    assert "Your registration completed" in driver.page_source


    # Step 2: Navigate to Books > Computing and Internet
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Books"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Computing and Internet"))).click()

    # Step 3: Validate page URL
    assert "computing-and-internet" in driver.current_url

    # Step 4: Click "Add to cart"
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart']"))).click()

    # Step 5: Click "Email a friend"
    # Open Email a Friend form
    driver.find_element(By.XPATH, "//input[@value='Email a friend']").click()

    # Fill the form
    driver.find_element(By.XPATH, "//input[@id='FriendEmail']").send_keys("nilaj@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='YourEmailAddress']").send_keys("")
    driver.find_element(By.XPATH, "//textarea[@id='PersonalMessage']").send_keys("Check this out!")

    # Submit the form
    driver.find_element(By.XPATH, "//input[@name='send-email']").click()

    # Step: Return to product page (in case email flow navigated away)
    # Return to product page directly instead of back
    driver.get("https://demowebshop.tricentis.com/computing-and-internet")

    # Step 6.5: After Email a Friend, click "Add to compare list"
    compare_xpath = "//input[contains(@class, 'add-to-compare-list-button')]"
    wait.until(EC.presence_of_element_located((By.XPATH, compare_xpath))).click()

#Books category filtering and sorting
def test_books_category_filtering_and_sorting(driver):
    driver.get("https://demowebshop.tricentis.com/books")
    wait = WebDriverWait(driver, 10)

    # Helper function to click dropdown option by visible text
    def select_dropdown_option(dropdown_xpath, option_text):
        wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
        wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, f"{dropdown_xpath}/option[text()='{option_text}']"))).click()

    # Step 1: Sort by - Position, Name: A to Z, Price: Low to High, Created on
    sort_xpath = "//select[@id='products-orderby']"
    sort_options = ['Position', 'Name: A to Z', 'Price: Low to High', 'Created on']
    for option in sort_options:
        select_dropdown_option(sort_xpath, option)

    # Step 2: Display - 4, 8, 12
    display_xpath = "//select[@id='products-pagesize']"
    display_options = ['4', '8', '12']
    for option in display_options:
        select_dropdown_option(display_xpath, option)

    # Step 3: View as - List, Grid
    view_xpath = "//select[@id='products-viewmode']"
    view_options = ['List', 'Grid']
    for option in view_options:
        select_dropdown_option(view_xpath, option)

    # Select Created on
    sort_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='products-orderby']")))
    sort_dropdown.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='products-orderby']/option[text()='Created on']"))).click()

    # Re-locate dropdown again after DOM update
    sort_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='products-orderby']")))
    sort_dropdown.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='products-orderby']/option[text()='Name: Z to A']"))).click()

#Full cart workflow    
def test_full_cart_workflow(driver):
    wait = WebDriverWait(driver, 10)

    # Step 1: Login
    driver.get("https://demowebshop.tricentis.com/")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))).click()
    wait.until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys("nilaj@gmail.com")
    driver.find_element(By.NAME, "Password").send_keys("Nila123")
    driver.find_element(By.XPATH, "//input[@class='button-1 login-button']").click()

    # Step 2: Search and click Health Book
    search_box = wait.until(EC.presence_of_element_located((By.ID, "small-searchterms")))
    search_box.clear()
    search_box.send_keys("Health Book")
    driver.find_element(By.XPATH, "//input[@value='Search']").click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Health Book"))).click()

    # Step 3: Add to cart
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart']"))).click()

    # Step 4: Go to Cart
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='cart-label']"))).click()

    # Step 5: From cart, click 'Health Book' again
    health_book_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td/a[text()='Health Book']]")))
    health_book_link = health_book_row.find_element(By.XPATH, ".//a[text()='Health Book']")
    health_book_link.click()

    # Step 6: Return to cart again
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='cart-label']"))).click()

   # Step 7: Remove only Health Book
    health_book_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td/a[text()='Health Book']]")))
    remove_checkbox = health_book_row.find_element(By.NAME, "removefromcart")
    remove_checkbox.click()
    driver.find_element(By.NAME, "updatecart").click()

    # Step 8: Estimate shipping
    driver.find_element(By.ID, "CountryId").send_keys("India")
    driver.find_element(By.ID, "ZipPostalCode").send_keys("612504")
    driver.find_element(By.NAME, "estimateshipping").click()

    # Step 9: Agree to terms of service
    wait.until(EC.element_to_be_clickable((By.ID, "termsofservice"))).click()

     # Step 10: Proceed to checkout and confirm checkout page
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.url_contains("checkout"))
    assert "checkout" in driver.current_url

   # ✅ Test 1: Home page should load with categories
@pytest.mark.order(1)
def test_homepage_loads(driver):
    driver.get("https://demowebshop.tricentis.com/")
    assert "Demo Web Shop" in driver.title


# ✅ Test 2: Check if all main categories are present
@pytest.mark.order(2)
def test_categories_present(driver):
    driver.get("https://demowebshop.tricentis.com/")
    top_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='top-menu']//a"))
    )
    category_names = [cat.text.strip() for cat in top_menu if cat.text.strip()]
    print(f"✅ Categories found: {category_names}")
    assert "books" in [c.lower() for c in category_names]


# ✅ Test 3: Click on BOOKS category and verify navigation
@pytest.mark.order(3)
def test_books_category_navigation(driver):
    driver.get("https://demowebshop.tricentis.com/")
    
    # Search for 'Health Book'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
    )
    search_box.send_keys("Health Book")
    search_box.submit()

    # Click the product link from search results using XPath
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[@class='product-title']/a[contains(text(),'Health Book')]"))
    )
    product_link.click()

    # Click Add to Cart button on product page using XPath
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart' and contains(@class,'add-to-cart-button')]"))
    )
    add_to_cart_btn.click()

    # Verify confirmation message using XPath
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='content']"))
    )
    assert "The product has been added to your shopping cart" in confirmation.text

    print("✅ Product added to cart successfully via XPath!")


# ✅ Test 4: Select first product in BOOKS and check product detail page
@pytest.mark.order(4)
def test_books_first_product(driver):
    driver.get("https://demowebshop.tricentis.com/books")
    first_product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='product-item']//h2/a"))
    )
    product_name = first_product.text
    first_product.click()

    # Wait for product detail page
    product_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='product-name']/h1"))
    )
    assert product_name in product_heading.text


# ✅ Test 5: Negative Test — Try finding a non-existent category (should fail)
@pytest.mark.order(5)
def test_invalid_category_link(driver):
    driver.get("https://demowebshop.tricentis.com/")
    with pytest.raises(Exception):
        driver.find_element(By.XPATH, "//ul[@class='top-menu']//a[text()='NonExistent']").click()
#---------------------------NEGATIVE TESTCASES----------------------------------------------------------
#Broken Footer Link
def test_broken_footer_link(driver):
    # Navigate to the Demowebshop homepage
    driver.get("https://demowebshop.tricentis.com/")

    # Click on the first footer link
    driver.find_element(By.XPATH, "//div[@class='footer']//ul/li[1]/a").click()

    # Wait for the page to load and verify the current URL
    WebDriverWait(driver, 10).until(EC.url_to_be("https://demowebshop.tricentis.com/no-such-page"))

    # Verify that the current URL is the expected broken link URL
    assert driver.current_url == "https://demowebshop.tricentis.com/no-such-page"

    # Wait for the page to load and verify the current URL again
    WebDriverWait(driver, 10).until(EC.url_to_be("https://demowebshop.tricentis.com/no-such-page"))

    # Verify that the current URL is still the expected broken link URL
    assert driver.current_url == "https://demowebshop.tricentis.com/no-such-page"

#Checkout without login
def test_checkout_without_login_should_fail():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/cart")
    try:
        driver.find_element(By.XPATH, "//input[@value='Checkout']").click()
    except:
        pass

    # Wrong expectation - checkout should redirect to login
    assert "Thank you" in driver.page_source
    driver.quit()

#Login with wrong password
def test_login_with_wrong_password_fails():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/login")
    driver.find_element(By.ID, "Email").send_keys("fakeuser@mail.com")
    driver.find_element(By.ID, "Password").send_keys("WrongPassword")
    driver.find_element(By.XPATH, "//input[@value='Log in']").click()
    
    # Deliberate wrong assertion: checking for "My account"
    assert "My account" in driver.page_source
    driver.quit()

#Newsletter ivalid email
def test_newsletter_invalid_email():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.ID, "newsletter-email").send_keys("invalid-email")
    driver.find_element(By.ID, "newsletter-subscribe-button").click()

    # Deliberately expecting a "Thank you" message
    assert "Thank you for signing up!" in driver.page_source
    driver.quit()

#Register with blank fields
def test_registration_with_blank_fields():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/register")
    driver.find_element(By.ID, "register-button").click()
    
    # This will FAIL because no error message is asserted
    assert "Your registration completed" in driver.page_source
    driver.quit()

#Search with special character
def test_search_non_existing_product():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/")
    driver.find_element(By.ID, "small-searchterms").send_keys("asdasd12#%!")
    driver.find_element(By.XPATH, "//input[@value='Search']").click()

    # Deliberately wrong assertion
    assert "Apple MacBook" in driver.page_source
    driver.quit()