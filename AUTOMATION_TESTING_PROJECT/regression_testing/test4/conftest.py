import pytest
import allure
import os
from datetime import datetime
from selenium import webdriver

@pytest.fixture(scope="function")
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    request.node.driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Let other hooks run and get the result
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = getattr(item, "driver", None)
        if driver:
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            driver.save_screenshot(filepath)

            # Attach to Allure
            with open(filepath, "rb") as image_file:
                allure.attach(image_file.read(), name=filename, attachment_type=allure.attachment_type.PNG)