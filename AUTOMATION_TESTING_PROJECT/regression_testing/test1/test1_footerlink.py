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


