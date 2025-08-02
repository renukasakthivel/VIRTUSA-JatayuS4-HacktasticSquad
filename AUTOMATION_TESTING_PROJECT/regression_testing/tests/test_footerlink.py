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

def test_footer_links():
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com/")
    driver.maximize_window()

    try:
        all_footer_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='footer']//ul//li/a"))
        )
    except:
        pytest.fail("Footer links did not load in time")

    # Filter out 'Follow us' links
    follow_us_domains = ["facebook.com", "twitter.com", "youtube.com", "rss", "google.com"]
    footer_links = [link for link in all_footer_links if not any(domain in link.get_attribute("href").lower() for domain in follow_us_domains)]

    for i in range(len(footer_links)):
        # Re-locate after each click
        footer_links = driver.find_elements(By.XPATH, "//div[@class='footer']//ul//li/a")
        filtered_links = [link for link in footer_links if not any(domain in link.get_attribute("href").lower() for domain in follow_us_domains)]

        link = filtered_links[i]
        href = link.get_attribute("href")
        link_text = link.text.strip()

        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        link.click()

        try:
            WebDriverWait(driver, 10).until(EC.url_contains(href.split("/")[-1]))
            print(f"✅ Verified footer link: {link_text} -> {href}")
        except:
            print(f"⚠️ Warning: Link '{link_text}' opened but validation failed.")

        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='footer']//ul//li/a")))

    driver.quit()




