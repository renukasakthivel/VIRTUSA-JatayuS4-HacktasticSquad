import time
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

@pytest.mark.parametrize(
    "friend_email, personal_message",
    [
        ("friend1@example.com", "Hey! Check this book out."),
        ("nilaj@gmail.com", "Try this book!"),
        ("test+123@mail.com", "You might like this."),
    ]
)
def test_computing_and_internet_page_interactivity(driver, friend_email, personal_message):
    wait = WebDriverWait(driver, 10)

    # Step 1: Open homepage
    driver.get("https://demowebshop.tricentis.com/")

    # Step 2: Register a new user
    driver.get("https://demowebshop.tricentis.com/register")
    wait.until(EC.element_to_be_clickable((By.ID, "gender-male"))).click()
    driver.find_element(By.ID, "FirstName").send_keys("Test")
    driver.find_element(By.ID, "LastName").send_keys("User")

    unique_email = f"testuser_{int(time.time())}@mail.com"
    driver.find_element(By.ID, "Email").send_keys(unique_email)
    driver.find_element(By.ID, "Password").send_keys("Password123!")
    driver.find_element(By.ID, "ConfirmPassword").send_keys("Password123!")
    driver.find_element(By.ID, "register-button").click()

    assert "Your registration completed" in driver.page_source

    # Step 3: Navigate to Books > Computing and Internet
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Books"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Computing and Internet"))).click()

    assert "computing-and-internet" in driver.current_url

    # Step 4: Add to cart
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Add to cart']"))).click()

    # Step 5: Click "Email a friend"
    driver.find_element(By.XPATH, "//input[@value='Email a friend']").click()
    driver.find_element(By.ID, "FriendEmail").send_keys(friend_email)
    driver.find_element(By.ID, "PersonalMessage").send_keys(personal_message)
    driver.find_element(By.NAME, "send-email").click()

    # You can assert success or error message
    result_text = driver.find_element(By.CLASS_NAME, "result").text
    assert "Your message has been sent" in result_text or "only registered customers can use email a friend feature" in result_text
