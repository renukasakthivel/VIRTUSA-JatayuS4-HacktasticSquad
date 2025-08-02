import os
from groq import Groq

def generate_prompt(test_type, fields, url, additional):
    prompt_lines = [
        f"Generate a robust Pytest + Selenium automation script for a *{test_type.lower()}* web form located at: {url}",
        "",
        "### Form Fields Found on the Page:"
    ]

    for i, field in enumerate(fields, start=1):
        label = field.get("label") or field.get("name") or field.get("id") or "Unnamed Field"
        field_type = field.get("type") or field.get("tag") or "Unknown Type"
        prompt_lines.append(f"{i}. *{label}* ({field_type})")

    prompt_lines.append("")
    prompt_lines.append("### Additional Testing Instructions / Conditions:")
    prompt_lines.append(additional if additional else "None provided.")

    if "login" in test_type.lower() or "username" in additional.lower() or "password" in additional.lower():
        prompt_lines.append("\n### Note:")
        prompt_lines.append("If the form requires login, include logic to enter username and password and submit the form.")

    return "\n".join(prompt_lines)


def generate_test_case(prompt, browser="chrome", driver_path=""):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Python expert that generates Pytest + Selenium test scripts "
                        "using a fixture-based WebDriver setup (called 'driver') for test execution. "
                        "Do NOT create a new WebDriver instance inside the test function. "
                        "Use WebDriverWait and proper locators (id, name, class, xpath). "
                        "Only validate driver.current_url (no other assertions). "
                        "Do not use try/except blocks. "
                        "Do not include imports or fixture code. "
                        "Only return the test function using the 'driver' fixture."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        generated_test_function = response.choices[0].message.content.strip()

        # ✅ Dynamic fixture for browser support
        screenshot_support = f'''import pytest
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
    browser = "{browser.lower()}"
    driver_path = r"{driver_path}"

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
        raise ValueError(f"Unsupported browser: {{browser}}")

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
            file_name = f"{{item.name}}.png"
            screenshot_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved to: {{screenshot_path}}")
'''

        final_code = screenshot_support + "\n\n" + generated_test_function
        return final_code

    except Exception as e:
        return f"# ❌ Error generating test case:\n# {str(e)}"