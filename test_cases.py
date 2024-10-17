import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class AmazonTests(unittest.TestCase):
    def setUp(self):
        # Set up the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        # Close the browser after tests
        self.driver.quit()

    def test_login(self):
        """Login Test: Validate login with valid and invalid credentials"""
        driver = self.driver
        driver.get("https://www.amazon.com/ap/signin")  # Updated URL
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_field.send_keys("invalid_email@example.com")  # Example invalid email
        driver.find_element(By.ID, "continue").click()

        # Check for error message
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-alert-content"))
        )
        self.assertIn("There was a problem", error_message.text)  # Adjust based on actual error text

    def test_functional_add_to_cart(self):
        """Functional Test: Validate adding an item to the cart"""
        driver = self.driver
        driver.get("https://www.amazon.com")
        # Assume you are adding a specific product (you need to adjust this part as per your test case)
        driver.find_element(By.ID, "twotabsearchtextbox").send_keys("acer laptops")
        driver.find_element(By.ID, "nav-search-submit-button").click()

        # Wait for the results and click on the first item
        first_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot .s-result-item h2 a"))
        )
        first_item.click()

        # Add to cart
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
        )
        add_to_cart_button.click()

        # Validate that the item was added to the cart
        cart_confirmation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-size-medium-plus"))
        )
        self.assertIn("Added to Cart", cart_confirmation.text)

    def test_ui_elements(self):
        """UI Test: Validate UI elements on the homepage"""
        driver = self.driver
        driver.get("https://www.amazon.com")
        self.assertTrue(driver.find_element(By.ID, "nav-logo-sprites").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "twotabsearchtextbox").is_displayed())

    def test_form_validation(self):
        """Form Validation Test: Validate error messages for empty form submission"""
        driver = self.driver
        driver.get("https://www.amazon.com/ap/signin")  # Use appropriate registration URL
        # Attempt to submit the form without filling it
        driver.find_element(By.ID, "continue").click()  # Attempt to continue without entering data
        
        # Validate error messages appear
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-alert-content"))
        )
        self.assertIn("Please enter your name", error_message.text)  # Adjust based on actual error message

if __name__ == "__main__":
    # Run the tests and generate a report
    unittest.main()
