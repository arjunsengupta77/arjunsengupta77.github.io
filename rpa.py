from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# Optional: use your actual path to msedgedriver if not in PATH
# service = EdgeService(executable_path="C:/path/to/msedgedriver.exe")
# driver = webdriver.Edge(service=service)

# If Edge WebDriver is in PATH:
driver = webdriver.Edge()

try:
    # Step 1: Go to the initial URL
    driver.get("https://example.com")

    # Step 2: Click the div with specific text
    clickable_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue']"))
    )
    clickable_div.click()

    # Step 3: Click hyperlink with specific text
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Target Page Link"))
    )
    link.click()

    # Step 4: Modify form fields
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "formElementId"))
    )

    driver.find_element(By.NAME, "username").send_keys("John Doe")

    age_field = driver.find_element(By.NAME, "age")
    age_field.clear()
    age_field.send_keys("30")

    country_select = Select(driver.find_element(By.NAME, "country"))
    country_select.select_by_visible_text("India")

    # Step 5: Click the save button
    driver.find_element(By.ID, "saveButton").click()

    time.sleep(3)

finally:
    driver.quit()