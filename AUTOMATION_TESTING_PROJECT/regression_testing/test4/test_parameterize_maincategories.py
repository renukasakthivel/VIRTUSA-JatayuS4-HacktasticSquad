import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://demowebshop.tricentis.com/")
    yield driver
    driver.quit()

@pytest.mark.parametrize("category_text, expected_url_part", [
    ("Books", "books"),
    ("Computers", "computers"),
    ("Electronics", "electronics"),
    ("Apparel & Shoes", "apparel-shoes"),
    ("Digital downloads", "digital-downloads"),
    ("Jewelry", "jewelry"),
    ("Gift Cards", "gift-cards"),
])
def test_main_category_navigation(driver, category_text, expected_url_part):
    wait = WebDriverWait(driver, 10)

    # Locate and click the category by link text
    category_link_xpath = f"//ul[@class='top-menu']//a[normalize-space(text())='{category_text}']"
    category_link = wait.until(EC.element_to_be_clickable((By.XPATH, category_link_xpath)))
    category_link.click()

    # Assertion: Validate that the correct category page is opened
    assert expected_url_part in driver.current_url, f"Failed to navigate to {category_text} category"
