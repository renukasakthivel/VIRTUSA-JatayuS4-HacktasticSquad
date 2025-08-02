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
from time import sleep, time

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
    

