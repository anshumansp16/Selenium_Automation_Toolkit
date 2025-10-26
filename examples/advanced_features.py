"""
Advanced Selenium Features Demo
Demonstrates: JavaScript execution, screenshots, cookies, scrolling, local storage
"""

import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import managed_driver


class AdvancedFeaturesPage:
    """Page Object for demonstrating advanced Selenium features"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.screenshot_dir = "screenshots"

        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            print(f"Created screenshots directory: {self.screenshot_dir}")

    def javascript_execution_demo(self):
        """
        Demonstrates executing JavaScript in the browser
        """
        print("\n=== JavaScript Execution Demo ===")
        self.driver.get("https://www.example.com")

        try:
            # 1. Get page information via JavaScript
            print("\n1. Getting page information via JavaScript:")
            title = self.driver.execute_script("return document.title;")
            print(f"   Page title: {title}")

            url = self.driver.execute_script("return window.location.href;")
            print(f"   Current URL: {url}")

            # 2. Modify page content
            print("\n2. Modifying page content:")
            original_heading = self.driver.find_element(By.TAG_NAME, "h1").text
            print(f"   Original heading: {original_heading}")

            self.driver.execute_script(
                "document.querySelector('h1').textContent = 'Modified by Selenium!';"
            )

            new_heading = self.driver.find_element(By.TAG_NAME, "h1").text
            print(f"   Modified heading: {new_heading}")

            # 3. Create new element
            print("\n3. Creating new element via JavaScript:")
            self.driver.execute_script("""
                var div = document.createElement('div');
                div.id = 'selenium-created';
                div.style.backgroundColor = 'lightblue';
                div.style.padding = '20px';
                div.style.margin = '20px';
                div.textContent = 'This element was created by Selenium!';
                document.body.appendChild(div);
            """)

            created_element = self.driver.find_element(By.ID, "selenium-created")
            print(f"   Created element text: {created_element.text}")

            # 4. Return complex data
            print("\n4. Getting browser information:")
            browser_info = self.driver.execute_script("""
                return {
                    userAgent: navigator.userAgent,
                    platform: navigator.platform,
                    language: navigator.language,
                    cookieEnabled: navigator.cookieEnabled,
                    windowSize: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    }
                };
            """)

            print(f"   Platform: {browser_info['platform']}")
            print(f"   Language: {browser_info['language']}")
            print(f"   Cookies Enabled: {browser_info['cookieEnabled']}")
            print(f"   Window Size: {browser_info['windowSize']['width']}x{browser_info['windowSize']['height']}")

            print("\n✓ JavaScript execution demonstration successful!")

        except Exception as e:
            print(f"✗ JavaScript execution demo failed: {e}")

    def scrolling_demo(self):
        """
        Demonstrates different scrolling techniques
        """
        print("\n=== Scrolling Demo ===")
        self.driver.get("https://www.selenium.dev/documentation/")

        try:
            # 1. Scroll to bottom of page
            print("\n1. Scrolling to bottom of page...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            scroll_position = self.driver.execute_script("return window.pageYOffset;")
            print(f"   Scroll position: {scroll_position}px from top")

            # 2. Scroll to top
            print("\n2. Scrolling to top of page...")
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            # 3. Scroll to specific element
            print("\n3. Scrolling to specific element...")
            try:
                # Find a footer element
                footer = self.driver.find_element(By.TAG_NAME, "footer")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", footer)
                time.sleep(1)
                print("   ✓ Scrolled to footer")
            except Exception:
                print("   Could not find footer element")

            # 4. Smooth scrolling
            print("\n4. Smooth scrolling demonstration...")
            self.driver.execute_script("""
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            """)
            time.sleep(2)

            print("✓ Scrolling demonstration successful!")

        except Exception as e:
            print(f"✗ Scrolling demo failed: {e}")

    def screenshot_demo(self):
        """
        Demonstrates taking screenshots
        """
        print("\n=== Screenshot Demo ===")
        self.driver.get("https://www.example.com")

        try:
            # 1. Full page screenshot
            print("\n1. Taking full page screenshot...")
            screenshot_path = os.path.join(self.screenshot_dir, "full_page.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"   ✓ Screenshot saved: {screenshot_path}")

            # 2. Element screenshot
            print("\n2. Taking element screenshot...")
            heading = self.driver.find_element(By.TAG_NAME, "h1")
            element_path = os.path.join(self.screenshot_dir, "heading_element.png")
            heading.screenshot(element_path)
            print(f"   ✓ Element screenshot saved: {element_path}")

            # 3. Screenshot with timestamp
            print("\n3. Taking timestamped screenshot...")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            timestamp_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp}.png")
            self.driver.save_screenshot(timestamp_path)
            print(f"   ✓ Timestamped screenshot saved: {timestamp_path}")

            # 4. Screenshot as base64 (useful for embedding in reports)
            print("\n4. Getting screenshot as base64...")
            screenshot_base64 = self.driver.get_screenshot_as_base64()
            print(f"   ✓ Base64 screenshot (first 50 chars): {screenshot_base64[:50]}...")

            print("\n✓ Screenshot demonstration successful!")
            print(f"\nAll screenshots saved in: {os.path.abspath(self.screenshot_dir)}")

        except Exception as e:
            print(f"✗ Screenshot demo failed: {e}")

    def cookies_demo(self):
        """
        Demonstrates cookie manipulation
        """
        print("\n=== Cookies Demo ===")
        self.driver.get("https://www.example.com")

        try:
            # 1. Add cookies
            print("\n1. Adding custom cookies...")
            self.driver.add_cookie({
                "name": "test_cookie",
                "value": "selenium_automation",
                "path": "/"
            })

            self.driver.add_cookie({
                "name": "user_id",
                "value": "12345",
                "path": "/"
            })

            print("   ✓ Added 2 cookies")

            # 2. Get all cookies
            print("\n2. Getting all cookies...")
            all_cookies = self.driver.get_cookies()
            print(f"   Total cookies: {len(all_cookies)}")
            for cookie in all_cookies:
                print(f"   - {cookie['name']}: {cookie['value']}")

            # 3. Get specific cookie
            print("\n3. Getting specific cookie...")
            test_cookie = self.driver.get_cookie("test_cookie")
            if test_cookie:
                print(f"   test_cookie value: {test_cookie['value']}")

            # 4. Delete specific cookie
            print("\n4. Deleting specific cookie...")
            self.driver.delete_cookie("test_cookie")
            print("   ✓ Deleted 'test_cookie'")

            remaining = len(self.driver.get_cookies())
            print(f"   Remaining cookies: {remaining}")

            # 5. Delete all cookies
            print("\n5. Deleting all cookies...")
            self.driver.delete_all_cookies()
            print(f"   Cookies after deletion: {len(self.driver.get_cookies())}")

            print("\n✓ Cookie manipulation demonstration successful!")

        except Exception as e:
            print(f"✗ Cookies demo failed: {e}")

    def local_storage_demo(self):
        """
        Demonstrates local storage manipulation
        """
        print("\n=== Local Storage Demo ===")
        self.driver.get("https://www.example.com")

        try:
            # 1. Set items in local storage
            print("\n1. Setting items in local storage...")
            self.driver.execute_script(
                "window.localStorage.setItem('username', 'selenium_user');"
            )
            self.driver.execute_script(
                "window.localStorage.setItem('theme', 'dark');"
            )
            print("   ✓ Set 2 items in local storage")

            # 2. Get items from local storage
            print("\n2. Getting items from local storage...")
            username = self.driver.execute_script(
                "return window.localStorage.getItem('username');"
            )
            theme = self.driver.execute_script(
                "return window.localStorage.getItem('theme');"
            )
            print(f"   username: {username}")
            print(f"   theme: {theme}")

            # 3. Get all local storage items
            print("\n3. Getting all local storage items...")
            all_items = self.driver.execute_script("""
                var items = {};
                for (var i = 0; i < localStorage.length; i++) {
                    var key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
            """)
            print(f"   Total items: {len(all_items)}")
            for key, value in all_items.items():
                print(f"   - {key}: {value}")

            # 4. Remove specific item
            print("\n4. Removing specific item...")
            self.driver.execute_script("window.localStorage.removeItem('theme');")
            print("   ✓ Removed 'theme'")

            # 5. Clear all local storage
            print("\n5. Clearing all local storage...")
            self.driver.execute_script("window.localStorage.clear();")
            remaining = self.driver.execute_script("return localStorage.length;")
            print(f"   Items after clear: {remaining}")

            print("\n✓ Local storage demonstration successful!")

        except Exception as e:
            print(f"✗ Local storage demo failed: {e}")

    def page_info_demo(self):
        """
        Demonstrates getting page information
        """
        print("\n=== Page Information Demo ===")
        self.driver.get("https://www.selenium.dev/")

        try:
            print("\n1. Basic page information:")
            print(f"   Title: {self.driver.title}")
            print(f"   Current URL: {self.driver.current_url}")

            # Get page source length
            page_source = self.driver.page_source
            print(f"   Page source length: {len(page_source)} characters")

            # Get loaded state
            print("\n2. Document ready state:")
            ready_state = self.driver.execute_script("return document.readyState;")
            print(f"   Document ready state: {ready_state}")

            # Get all links
            print("\n3. Page statistics:")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            print(f"   Total links: {len(links)}")

            images = self.driver.find_elements(By.TAG_NAME, "img")
            print(f"   Total images: {len(images)}")

            # Get viewport size
            viewport = self.driver.execute_script("""
                return {
                    width: Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
                    height: Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
                };
            """)
            print(f"   Viewport size: {viewport['width']}x{viewport['height']}")

            print("\n✓ Page information gathering successful!")

        except Exception as e:
            print(f"✗ Page info demo failed: {e}")


def main():
    """Main execution function"""

    print("="*60)
    print("Advanced Selenium Features Demonstration")
    print("JavaScript, Screenshots, Cookies, Scrolling, Local Storage")
    print("="*60)

    with managed_driver('chrome', headless=False) as driver:
        driver.maximize_window()

        page = AdvancedFeaturesPage(driver)

        try:
            # 1. JavaScript execution
            page.javascript_execution_demo()
            input("\nPress Enter to continue to next demo...")

            # 2. Scrolling
            page.scrolling_demo()
            input("\nPress Enter to continue to next demo...")

            # 3. Screenshots
            page.screenshot_demo()
            input("\nPress Enter to continue to next demo...")

            # 4. Cookies
            page.cookies_demo()
            input("\nPress Enter to continue to next demo...")

            # 5. Local Storage
            page.local_storage_demo()
            input("\nPress Enter to continue to next demo...")

            # 6. Page Information
            page.page_info_demo()

            print("\n" + "="*60)
            print("✓ All advanced features demonstrations completed!")
            print("="*60)

        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user")
        except Exception as e:
            print(f"\n\n✗ Demo failed: {e}")


if __name__ == "__main__":
    main()
