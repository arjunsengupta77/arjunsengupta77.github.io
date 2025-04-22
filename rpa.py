from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the driver (using Chrome here)
driver = webdriver.Chrome()

try:
    # Step 1: Open the browser and navigate to the URL
    driver.get("https://example.com")

    # Step 2: Wait for and click the button to go to new page
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nextPageButton"))
    )
    button.click()

    # Step 3: Find hyperlink with specific text and click it
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Target Page Link"))
    )
    link.click()

    # Step 4: Wait for form to load and fill it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "formElementId"))
    )

    # Modify text field
    text_input = driver.find_element(By.NAME, "username")
    text_input.clear()
    text_input.send_keys("John Doe")

    # Modify number field
    number_input = driver.find_element(By.NAME, "age")
    number_input.clear()
    number_input.send_keys("30")

    # Select from dropdown
    dropdown = Select(driver.find_element(By.NAME, "country"))
    dropdown.select_by_visible_text("India")

    # Step 5: Click the save button
    save_button = driver.find_element(By.ID, "saveButton")
    save_button.click()

    # Wait a moment to observe result
    time.sleep(3)

finally:
    driver.quit()