"""
Form Automation Example
Demonstrates common form interactions: text input, dropdowns, checkboxes, radio buttons
"""

import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import managed_driver


class FormPage:
    """Page Object for form automation"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def fill_text_input(self, locator, text, clear_first=True):
        """
        Fill text input field

        Args:
            locator: Element locator tuple (By.TYPE, "value")
            text: Text to enter
            clear_first: Clear field before entering text
        """
        element = self.wait.until(EC.presence_of_element_located(locator))
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def select_dropdown_by_text(self, locator, text):
        """
        Select dropdown option by visible text

        Args:
            locator: Select element locator
            text: Visible text to select
        """
        select_element = self.wait.until(EC.presence_of_element_located(locator))
        select = Select(select_element)
        select.select_by_visible_text(text)
        return select

    def select_dropdown_by_value(self, locator, value):
        """
        Select dropdown option by value attribute

        Args:
            locator: Select element locator
            value: Value attribute to select
        """
        select_element = self.wait.until(EC.presence_of_element_located(locator))
        select = Select(select_element)
        select.select_by_value(value)
        return select

    def select_dropdown_by_index(self, locator, index):
        """
        Select dropdown option by index

        Args:
            locator: Select element locator
            index: Index to select (0-based)
        """
        select_element = self.wait.until(EC.presence_of_element_located(locator))
        select = Select(select_element)
        select.select_by_index(index)
        return select

    def check_checkbox(self, locator):
        """
        Check a checkbox (only if not already checked)

        Args:
            locator: Checkbox element locator
        """
        checkbox = self.wait.until(EC.element_to_be_clickable(locator))
        if not checkbox.is_selected():
            checkbox.click()
        return checkbox

    def uncheck_checkbox(self, locator):
        """
        Uncheck a checkbox (only if currently checked)

        Args:
            locator: Checkbox element locator
        """
        checkbox = self.wait.until(EC.element_to_be_clickable(locator))
        if checkbox.is_selected():
            checkbox.click()
        return checkbox

    def select_radio_button(self, locator):
        """
        Select a radio button

        Args:
            locator: Radio button element locator
        """
        radio = self.wait.until(EC.element_to_be_clickable(locator))
        if not radio.is_selected():
            radio.click()
        return radio

    def click_button(self, locator):
        """
        Click a button

        Args:
            locator: Button element locator
        """
        button = self.wait.until(EC.element_to_be_clickable(locator))
        button.click()
        return button

    def upload_file(self, locator, file_path):
        """
        Upload a file

        Args:
            locator: File input element locator
            file_path: Absolute path to file
        """
        file_input = self.wait.until(EC.presence_of_element_located(locator))
        file_input.send_keys(file_path)
        return file_input

    def submit_form_with_enter(self, locator):
        """
        Submit form by pressing Enter on an input field

        Args:
            locator: Input element locator
        """
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.send_keys(Keys.RETURN)
        return element

    def get_selected_dropdown_text(self, locator):
        """
        Get currently selected dropdown option text

        Args:
            locator: Select element locator

        Returns:
            str: Selected option text
        """
        select_element = self.wait.until(EC.presence_of_element_located(locator))
        select = Select(select_element)
        return select.first_selected_option.text

    def is_checkbox_checked(self, locator):
        """
        Check if checkbox is selected

        Args:
            locator: Checkbox element locator

        Returns:
            bool: True if checked, False otherwise
        """
        checkbox = self.wait.until(EC.presence_of_element_located(locator))
        return checkbox.is_selected()


def example_form_automation():
    """
    Example demonstrating various form interactions

    This is a template - replace with your actual form locators and URL
    """

    with managed_driver('chrome', headless=False) as driver:
        form_page = FormPage(driver)

        # Navigate to your form
        driver.get("https://example.com/form")  # Replace with actual URL

        # Example: Fill text inputs
        # form_page.fill_text_input((By.ID, "firstName"), "John")
        # form_page.fill_text_input((By.ID, "lastName"), "Doe")
        # form_page.fill_text_input((By.NAME, "email"), "john.doe@example.com")

        # Example: Select from dropdown
        # form_page.select_dropdown_by_text((By.ID, "country"), "United States")

        # Example: Check checkboxes
        # form_page.check_checkbox((By.ID, "terms"))
        # form_page.check_checkbox((By.ID, "newsletter"))

        # Example: Select radio button
        # form_page.select_radio_button((By.ID, "male"))

        # Example: Upload file
        # form_page.upload_file((By.ID, "fileUpload"), "/path/to/file.pdf")

        # Example: Submit form
        # form_page.click_button((By.CSS_SELECTOR, "button[type='submit']"))

        print("Form automation example completed!")


def practical_google_form_example():
    """
    Practical example: Automating a Google search
    Demonstrates real-world form interaction
    """

    with managed_driver('chrome', headless=False) as driver:
        form_page = FormPage(driver)

        # Navigate to Google
        driver.get("https://www.google.com")

        # Find and fill search box
        search_input = (By.NAME, "q")
        form_page.fill_text_input(search_input, "Selenium Python automation")

        # Submit by pressing Enter
        form_page.submit_form_with_enter(search_input)

        # Wait for results
        results_locator = (By.ID, "search")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(results_locator)
        )

        print("✓ Google search completed successfully!")

        # Take screenshot (optional)
        # driver.save_screenshot("search_results.png")


if __name__ == "__main__":
    # Run the practical example
    practical_google_form_example()

    # Uncomment to run the template example
    # example_form_automation()
