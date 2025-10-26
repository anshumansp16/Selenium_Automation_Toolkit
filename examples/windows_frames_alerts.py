"""
Windows, Frames & Alerts Demo
Demonstrates: Multiple windows/tabs, iframe switching, alert handling
"""

import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import managed_driver


class WindowsFramesAlertsPage:
    """Page Object for demonstrating windows, frames, and alerts"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def multiple_windows_demo(self):
        """
        Demonstrates handling multiple browser windows/tabs
        """
        print("\n=== Multiple Windows Demo ===")
        self.driver.get("https://www.selenium.dev/selenium/web/window_switching_tests/page_with_frame.html")

        try:
            # Store original window handle
            original_window = self.driver.current_window_handle
            print(f"Original window handle: {original_window}")
            print(f"Original page title: {self.driver.title}")

            # Open new window using JavaScript
            print("\nOpening new window...")
            self.driver.execute_script("window.open('https://www.selenium.dev/documentation/', '_blank');")

            # Wait for new window
            self.wait.until(lambda d: len(d.window_handles) > 1)

            # Get all window handles
            all_windows = self.driver.window_handles
            print(f"Total windows: {len(all_windows)}")

            # Switch to new window
            for window in all_windows:
                if window != original_window:
                    print(f"\nSwitching to new window: {window}")
                    self.driver.switch_to.window(window)
                    break

            # Verify we're in the new window
            print(f"New window title: {self.driver.title}")
            print(f"New window URL: {self.driver.current_url}")

            # Do something in new window
            try:
                heading = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
                print(f"Found heading: {heading.text}")
            except TimeoutException:
                print("Could not find heading in new window")

            # Close new window
            print("\nClosing new window...")
            self.driver.close()

            # Switch back to original window
            print("Switching back to original window...")
            self.driver.switch_to.window(original_window)
            print(f"Back to: {self.driver.title}")

            print("✓ Multiple windows handling successful!")

        except Exception as e:
            print(f"✗ Multiple windows demo failed: {e}")
            # Ensure we're back to original window
            self.driver.switch_to.window(original_window)

    def iframe_demo(self):
        """
        Demonstrates switching between iframes
        """
        print("\n=== iFrame Demo ===")
        self.driver.get("https://www.w3schools.com/html/html_iframe.asp")

        try:
            # Find iframe
            print("Looking for iframe...")
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='W3Schools Free Online Web Tutorials']"))
            )
            print(f"Found iframe with src: {iframe.get_attribute('src')}")

            # Switch to iframe
            print("\nSwitching to iframe...")
            self.driver.switch_to.frame(iframe)

            # Interact with content inside iframe
            try:
                # Try to find an element inside the iframe
                iframe_heading = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
                print(f"Content inside iframe: {iframe_heading.text}")
            except TimeoutException:
                print("Could not find specific content in iframe")

            # Switch back to main content
            print("\nSwitching back to main content...")
            self.driver.switch_to.default_content()

            # Verify we're back in main content
            main_heading = self.driver.find_element(By.TAG_NAME, "h1")
            print(f"Main page heading: {main_heading.text}")

            print("✓ iframe switching successful!")

        except Exception as e:
            print(f"✗ iframe demo failed: {e}")
            self.driver.switch_to.default_content()

    def nested_iframes_demo(self):
        """
        Demonstrates handling nested iframes
        """
        print("\n=== Nested iFrames Demo ===")
        self.driver.get("https://www.selenium.dev/selenium/web/window_switching_tests/page_with_frame.html")

        try:
            # Switch to first iframe by index
            print("Switching to first iframe (by index 0)...")
            self.driver.switch_to.frame(0)

            # Try to find content in this iframe
            try:
                content = self.driver.find_element(By.TAG_NAME, "body")
                print(f"First iframe body text: {content.text[:50]}...")
            except Exception:
                print("Could not read iframe content")

            # Go back to parent frame
            print("\nSwitching to parent frame...")
            self.driver.switch_to.parent_frame()

            # Or go back to main content
            print("Switching to default content...")
            self.driver.switch_to.default_content()

            print("✓ Nested iframe navigation successful!")

        except Exception as e:
            print(f"✗ Nested iframe demo failed: {e}")
            self.driver.switch_to.default_content()

    def alert_demo(self):
        """
        Demonstrates handling JavaScript alerts
        Uses: https://www.w3schools.com/js/tryit.asp?filename=tryjs_alert
        """
        print("\n=== Alert Demo ===")
        self.driver.get("https://www.selenium.dev/selenium/web/alerts.html")

        try:
            # Simple alert
            print("\n1. Testing simple alert...")
            alert_button = self.driver.find_element(By.ID, "alert")
            alert_button.click()

            # Wait for alert and switch to it
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            print(f"   Alert text: {alert.text}")
            print("   Accepting alert...")
            alert.accept()
            print("   ✓ Alert accepted!")

        except NoAlertPresentException:
            print("   ✗ No alert found")
        except Exception as e:
            print(f"   ✗ Alert demo failed: {e}")

    def confirm_demo(self):
        """
        Demonstrates handling confirmation dialogs
        """
        print("\n=== Confirm Dialog Demo ===")
        self.driver.get("https://www.selenium.dev/selenium/web/alerts.html")

        try:
            # Confirm dialog - Accept
            print("\n1. Testing confirm dialog (Accept)...")
            confirm_button = self.driver.find_element(By.ID, "confirm")
            confirm_button.click()

            self.wait.until(EC.alert_is_present())
            confirm = self.driver.switch_to.alert

            print(f"   Confirm text: {confirm.text}")
            print("   Clicking OK...")
            confirm.accept()

            # Check result
            result = self.driver.find_element(By.ID, "confirm-result")
            print(f"   Result: {result.text}")

            # Confirm dialog - Dismiss
            print("\n2. Testing confirm dialog (Dismiss)...")
            confirm_button.click()

            self.wait.until(EC.alert_is_present())
            confirm = self.driver.switch_to.alert

            print("   Clicking Cancel...")
            confirm.dismiss()

            # Check result
            result = self.driver.find_element(By.ID, "confirm-result")
            print(f"   Result: {result.text}")

            print("   ✓ Confirm dialog handling successful!")

        except Exception as e:
            print(f"   ✗ Confirm demo failed: {e}")

    def prompt_demo(self):
        """
        Demonstrates handling prompt dialogs
        """
        print("\n=== Prompt Dialog Demo ===")
        self.driver.get("https://www.selenium.dev/selenium/web/alerts.html")

        try:
            print("\n1. Testing prompt dialog...")
            prompt_button = self.driver.find_element(By.ID, "prompt")
            prompt_button.click()

            # Wait for prompt
            self.wait.until(EC.alert_is_present())
            prompt = self.driver.switch_to.alert

            print(f"   Prompt text: {prompt.text}")

            # Send text to prompt
            test_text = "Selenium Automation"
            print(f"   Entering text: '{test_text}'")
            prompt.send_keys(test_text)

            print("   Accepting prompt...")
            prompt.accept()

            # Check result
            result = self.driver.find_element(By.ID, "prompt-result")
            print(f"   Result: {result.text}")

            # Test dismissing prompt
            print("\n2. Testing prompt dismissal...")
            prompt_button.click()

            self.wait.until(EC.alert_is_present())
            prompt = self.driver.switch_to.alert
            print("   Dismissing prompt...")
            prompt.dismiss()

            result = self.driver.find_element(By.ID, "prompt-result")
            print(f"   Result: {result.text}")

            print("   ✓ Prompt dialog handling successful!")

        except Exception as e:
            print(f"   ✗ Prompt demo failed: {e}")

    def window_size_demo(self):
        """
        Demonstrates window size manipulation
        """
        print("\n=== Window Size Demo ===")

        try:
            # Get current size
            current_size = self.driver.get_window_size()
            print(f"Current window size: {current_size['width']}x{current_size['height']}")

            # Set specific size
            print("\nSetting window size to 800x600...")
            self.driver.set_window_size(800, 600)
            new_size = self.driver.get_window_size()
            print(f"New size: {new_size['width']}x{new_size['height']}")

            import time
            time.sleep(1)

            # Maximize
            print("\nMaximizing window...")
            self.driver.maximize_window()
            max_size = self.driver.get_window_size()
            print(f"Maximized size: {max_size['width']}x{max_size['height']}")

            print("✓ Window size manipulation successful!")

        except Exception as e:
            print(f"✗ Window size demo failed: {e}")


def main():
    """Main execution function"""

    print("="*60)
    print("Windows, Frames & Alerts Demonstration")
    print("Showing window switching, iframe handling, and alerts")
    print("="*60)

    with managed_driver('chrome', headless=False) as driver:
        driver.maximize_window()

        page = WindowsFramesAlertsPage(driver)

        try:
            # 1. Multiple windows
            page.multiple_windows_demo()
            input("\nPress Enter to continue to next demo...")

            # 2. iFrame handling
            page.iframe_demo()
            input("\nPress Enter to continue to next demo...")

            # 3. Nested iframes
            page.nested_iframes_demo()
            input("\nPress Enter to continue to next demo...")

            # 4. Alerts
            page.alert_demo()
            input("\nPress Enter to continue to next demo...")

            # 5. Confirm dialogs
            page.confirm_demo()
            input("\nPress Enter to continue to next demo...")

            # 6. Prompt dialogs
            page.prompt_demo()
            input("\nPress Enter to continue to next demo...")

            # 7. Window size manipulation
            page.window_size_demo()

            print("\n" + "="*60)
            print("✓ All demonstrations completed successfully!")
            print("="*60)

        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user")
        except Exception as e:
            print(f"\n\n✗ Demo failed: {e}")


if __name__ == "__main__":
    main()
