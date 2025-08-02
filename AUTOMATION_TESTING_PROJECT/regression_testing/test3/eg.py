# @pytest.mark.parametrize("link_text", ["Register", "Log in", "Shopping cart", "Wishlist"])
# def test_top_section_links(driver, link_text):
#     driver.get("https://demowebshop.tricentis.com/")
#     driver.find_element(By.LINK_TEXT, link_text).click()
#     assert link_text.lower().replace(" ", "-") in driver.current_url


# # ✅ Test 3: Checkout Button without cart items
# def test_checkout_without_items(driver):
#     driver.get("https://demowebshop.tricentis.com/cart")
#     driver.find_element(By.NAME, "checkout").click()
#     assert "login" in driver.current_url or "register" in driver.page_source


# # ✅ Test 4: Order Confirmation Page (accessed after login)
# def test_order_confirmation_page(driver):
#     driver.get("https://demowebshop.tricentis.com/login")
#     driver.find_element(By.ID, "Email").send_keys("test@test.com")  # use real user
#     driver.find_element(By.ID, "Password").send_keys("Test@123")
#     driver.find_element(By.CSS_SELECTOR, "input.login-button").click()
#     driver.get("https://demowebshop.tricentis.com/checkout/completed")
#     assert "order has been successfully processed" in driver.page_source.lower()


# # ✅ Test 5: Add to Wishlist
# def test_add_to_wishlist(driver):
#     driver.get("https://demowebshop.tricentis.com/books")
#     driver.find_element(By.XPATH, "(//input[@value='Add to wishlist'])[1]").click()
#     assert "The product has been added to your wishlist" in driver.page_source


# # ✅ Test 6: Footer Link Validation
# @pytest.mark.parametrize("footer_text", ["Shipping & returns", "Privacy notice", "Conditions of use", "About us"])
# def test_footer_links(driver, footer_text):
#     driver.get("https://demowebshop.tricentis.com/")
#     driver.find_element(By.LINK_TEXT, footer_text).click()
#     assert footer_text.lower().replace(" ", "-") in driver.current_url


# # ✅ Test 7: Popular Tags
# @pytest.mark.parametrize("tag", ["awesome", "book", "cool"])
# def test_popular_tags(driver, tag):
#     driver.get("https://demowebshop.tricentis.com/")
#     wait = WebDriverWait(driver, 10)
#     tag_xpath = f"//div[@class='block block-popular-tags']//a[contains(text(), '{tag}')]"
#     tag_element = wait.until(EC.element_to_be_clickable((By.XPATH, tag_xpath)))
#     tag_element.click()
#     assert tag.lower() in driver.current_url


# # ✅ Test 8: Sort By, Display, View As dropdowns
# @pytest.mark.parametrize("sort_text", ["Position", "Name: A to Z", "Price: Low to High"])
# @pytest.mark.parametrize("display_count", ["4", "8", "12"])
# @pytest.mark.parametrize("view_as", ["Grid", "List"])
# def test_books_sort_display_view(driver, sort_text, display_count, view_as):
#     driver.get("https://demowebshop.tricentis.com/books")

#     Select(driver.find_element(By.ID, "products-orderby")).select_by_visible_text(sort_text)
#     Select(driver.find_element(By.ID, "products-pagesize")).select_by_visible_text(display_count)
#     Select(driver.find_element(By.ID, "products-viewmode")).select_by_visible_text(view_as)

#     assert True  # No crash = success for UI interaction

# @pytest.mark.parametrize("price_label", ["Under 25.00", "25.00 - 50.00", "Over 50.00"])
# def test_filter_by_price(driver, price_label):
#     driver.get("https://demowebshop.tricentis.com/books")
#     price_xpath = f"//ul[@class='price-range-selector']/li/a[contains(text(), '{price_label}')]"
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, price_xpath))).click()
#     assert price_label.lower().replace(" ", "-").replace(".", "") in driver.current_url
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("poll_option_id", [
    "pollanswers-1",  # Excellent
    "pollanswers-2"   # Good
])
def test_poll_submission(driver, base_url, poll_option_id):
    driver.get(base_url)
    
    # Wait for the poll option to appear and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, poll_option_id))
    ).click()

    # Submit the poll
    driver.find_element(By.ID, "vote-poll-1").click()

    # Assertion based on login status
    assert "Only registered users can vote." in driver.page_source or \
           "Thank you for voting!" in driver.page_source

