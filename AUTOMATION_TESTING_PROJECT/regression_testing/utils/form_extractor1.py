from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extract_all_elements(url, driver_path, browser="chrome", username=None, password=None):
    # 1. Browser setup
    if browser == "chrome":
        options = ChromeOptions()
        # options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        # options.add_argument("--headless=new")
        driver = webdriver.Edge(service=EdgeService(driver_path), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        # options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(driver_path), options=options)

    else:
        raise ValueError("Unsupported browser: " + browser)

    driver.get(url)

    # 2. Login if required
    if username and password:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
            time.sleep(2)
            username_field = driver.find_element(By.XPATH, "//input[@type='text' or contains(@name,'user')]")
            password_field = driver.find_element(By.XPATH, "//input[@type='password']")
            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(3)
        except Exception as e:
            print(f"Login failed: {e}")

    # 3. Wait for page to render
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)  # Allow JS content to fully load

    # 4. XPath generator (fixed)
    def get_xpath(el):
        return driver.execute_script("""
            function getXPath(element) {
                if (element.id !== '')
                    return '//*[@id="' + element.id + '"]';
                var path = [];
                while (element && element.nodeType === Node.ELEMENT_NODE) {
                    var index = 1;
                    var sibling = element.previousSibling;
                    while (sibling) {
                        if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === element.tagName) {
                            index++;
                        }
                        sibling = sibling.previousSibling;
                    }
                    path.unshift(element.tagName.toLowerCase() + '[' + index + ']');
                    element = element.parentNode;
                }
                return '/' + path.join('/');
            }
            return getXPath(arguments[0]);
        """, el)

    # 5. Extract info
    def extract_info(el):
        try:
            return {
                "tag": el.tag_name,
                "type": el.get_attribute("type") or el.tag_name,
                "name": el.get_attribute("name") or "",
                "id": el.get_attribute("id") or "",
                "class": el.get_attribute("class") or "",
                "placeholder": el.get_attribute("placeholder") or "",
                "value": el.get_attribute("value") or "",
                "text": el.text.strip(),
                "xpath": get_xpath(el) or ""
            }
        except:
            return None

    # 6. Tags to extract
    tags_to_extract = [
        "input", "textarea", "select", "button", "a", "div", "span", "label",
        "img", "h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li",
        "table", "thead", "tbody", "tr", "td", "th", "form", "iframe", "nav", "footer", "header"
    ]

    # 7. Extract visible elements
    elements = []

    def collect_elements_from_context():
        for tag in tags_to_extract:
            found_elements = driver.find_elements(By.TAG_NAME, tag)
            for el in found_elements:
                if el.is_displayed():
                    info = extract_info(el)
                    if info:
                        elements.append(info)

    # 8. Extract from main document
    collect_elements_from_context()

    # 9. Extract from iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)
            collect_elements_from_context()
            driver.switch_to.default_content()
        except:
            continue  # Skip if iframe can't be accessed

    driver.quit()
    return elements