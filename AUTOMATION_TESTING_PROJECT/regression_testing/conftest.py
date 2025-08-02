import pytest
from selenium import webdriver
import os

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)

    # Attach the driver to the node for access in hook
    request.node.driver = driver

    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = getattr(item, "driver", None)
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"{item.name}.png"
            screenshot_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved to: {screenshot_path}")