import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import allure
import os
from datetime import datetime


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome",
        help="Browser to run tests: chrome, firefox, or edge"
    )


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    if browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.maximize_window()
    request.node.driver = driver  # Attach driver to the request node
    yield driver
    driver.quit()


# Hook to detect test result and attach screenshot to Allure on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = getattr(item, "driver", None)
        if driver:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            test_name = item.name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)

            # Attach to Allure report
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"{test_name}_screenshot", attachment_type=allure.attachment_type.PNG)
