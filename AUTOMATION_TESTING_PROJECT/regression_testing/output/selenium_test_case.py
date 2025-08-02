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


```python
# test_footer_links.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def test_footer_links(driver):
    """
    Test footer links functionality on the demo web shop website.

    This test validates that each footer link is clearly visible, clickable, and
    navigates the user to the correct and intended web page without encountering
    errors such as 404 (page not found) or incorrect redirections.
    """
    # Scroll to the footer section
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Get all footer links
    footer_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='footer']//ul//li//a"))
    )

    # Iterate over each footer link
    for link in footer_links:
        # Get the link text and href
        link_text = link.text
        link_href = link.get_attribute("href")

        # Click the link
        link.click()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.title_contains(link_text))

        # Validate the URL
        assert driver.current_url == link_href

        # Scroll back to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.title_contains(link_text))

# pytest.ini
[pytest]
addopts = --browser=chrome --html=report.html --self-contained-html

[pytest-browser]
browser = chrome

[pytest-html]
report_title = Demo Web Shop Regression Suite

[pytest-selenium]
driver = webdriver-manager

[pytest-selenium-browser]
browser = chrome

[pytest-selenium-options]
--headless
--window-size=1920,1080

[pytest-selenium-flags]
--disable-gpu
--enable-logging
```

```python
# conftest.py
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

@pytest.fixture(scope="session", autouse=True)
def driver(request):
    """
    WebDriver fixture for Pytest.

    This fixture sets up a WebDriver instance based on the browser flag.
    """
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(GeckoDriverManager().install(), options=options)
    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)
    else:
        raise ValueError("Invalid browser flag. Please use --browser=chrome, firefox, or edge.")

    yield driver
    driver.quit()

    # Capture screenshots on failures
    if request.node.rep_setup.failed:
        driver.save_screenshot("screenshots/failed_setup.png")
    if request.node.rep_call.failed:
        driver.save_screenshot("screenshots/failed_test.png")
```

```python
# test_runner.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for testing. Options: chrome, firefox, edge",
    )

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: mark the test as slow to run",
    )

def pytest_sessionstart(session):
    # Set up the WebDriver instance
    driver = session.config.cache.get("driver")
    if driver:
        driver.maximize_window()
        driver.get("https://demowebshop.tricentis.com/")

def pytest_sessionfinish(session, exitstatus):
    # Close the WebDriver instance
    driver = session.config.cache.get("driver")
    if driver:
        driver.quit()

def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Test Steps"))

def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.nodeid))

def pytest_html_results_table_footer(cells):
    cells.append(html.tr(html.td("Total Tests: %s" % pytest.nodes)))
```

```python
# pytest.ini
[pytest]
addopts = --browser=chrome --html=report.html --self-contained-html

[pytest-browser]
browser = chrome

[pytest-html]
report_title = Demo Web Shop Regression Suite

[pytest-selenium]
driver = webdriver-manager

[pytest-selenium-browser]
browser = chrome

[pytest-selenium-options]
--headless
--window-size=1920,1080

[pytest-selenium-flags]
--disable-gpu
--enable-logging
```