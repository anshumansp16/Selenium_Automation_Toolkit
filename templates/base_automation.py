"""
Selenium Automation Boilerplate Template

Copy this file to start a new automation project.
Includes best practices: Page Object Model pattern, proper waits, and error handling.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import managed_driver


class BasePage:
    """Base page class with common functionality"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        wait_time = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {locator}")

    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait"""
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def click_element(self, locator, timeout=None):
        """Click element when clickable"""
        wait_time = timeout or self.timeout
        element = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def input_text(self, locator, text, clear_first=True):
        """Input text into element"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        """Get text from element"""
        return self.find_element(locator).text

    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False


class ExamplePage(BasePage):
    """
    Example Page Object Model class
    Define your page-specific locators and methods here
    """

    # Locators - Use constants for better maintainability
    SEARCH_INPUT = (By.ID, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESULT_ITEMS = (By.CLASS_NAME, "result-item")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com"

    def navigate(self):
        """Navigate to page"""
        self.driver.get(self.url)
        return self

    def search(self, query):
        """Perform search action"""
        self.input_text(self.SEARCH_INPUT, query)
        self.click_element(self.SEARCH_BUTTON)
        return self

    def get_results(self):
        """Get search results"""
        return self.find_elements(self.RESULT_ITEMS)


def main():
    """
    Main automation flow
    Replace with your automation logic
    """

    # Use context manager for automatic cleanup
    with managed_driver('chrome', headless=False) as driver:
        try:
            # Initialize page object
            page = ExamplePage(driver)

            # Navigation
            page.navigate()

            # Perform actions
            page.search("selenium automation")

            # Get results
            results = page.get_results()
            print(f"Found {len(results)} results")

            # Your automation logic here

        except Exception as e:
            print(f"Automation failed: {e}")
            raise


if __name__ == "__main__":
    main()
