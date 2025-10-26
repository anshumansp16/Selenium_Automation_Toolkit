"""
ActionChains Demo - Advanced Mouse & Keyboard Interactions
Demonstrates: Hover menus, drag & drop, key combinations, sliders
"""

import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import managed_driver


class ActionChainsPage:
    """Page Object for demonstrating ActionChains"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)

    def hover_menu_demo(self):
        """
        Demonstrates hovering over dropdown menus
        Uses: https://www.w3schools.com/howto/howto_css_dropdown_navbar.asp
        """
        print("\n=== Hover Menu Demo ===")
        self.driver.get("https://www.w3schools.com/howto/howto_css_dropdown_navbar.asp")

        try:
            # Wait for page to load
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "dropdown"))
            )

            # Find dropdown menu
            dropdown = self.driver.find_element(By.CLASS_NAME, "dropdown")

            # Hover over dropdown to reveal menu
            print("Hovering over 'Dropdown' menu...")
            self.actions.move_to_element(dropdown).perform()

            # Wait for dropdown content to appear
            dropdown_content = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-content"))
            )

            # Get menu items
            menu_items = dropdown_content.find_elements(By.TAG_NAME, "a")
            print(f"Found {len(menu_items)} menu items:")
            for item in menu_items:
                print(f"  - {item.text}")

            print("✓ Hover menu interaction successful!")

        except Exception as e:
            print(f"✗ Hover menu demo failed: {e}")

    def drag_drop_demo(self):
        """
        Demonstrates drag and drop functionality
        Uses: https://jqueryui.com/droppable/
        """
        print("\n=== Drag & Drop Demo ===")
        self.driver.get("https://jqueryui.com/droppable/")

        try:
            # Switch to iframe containing the demo
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "demo-frame"))
            )
            self.driver.switch_to.frame(iframe)

            # Find draggable and droppable elements
            draggable = self.wait.until(
                EC.presence_of_element_located((By.ID, "draggable"))
            )
            droppable = self.driver.find_element(By.ID, "droppable")

            print(f"Draggable text: {draggable.text}")
            print(f"Droppable text before: {droppable.text}")

            # Perform drag and drop
            print("Performing drag and drop...")
            self.actions.drag_and_drop(draggable, droppable).perform()

            # Verify drop was successful
            self.wait.until(
                EC.text_to_be_present_in_element((By.ID, "droppable"), "Dropped!")
            )

            print(f"Droppable text after: {droppable.text}")
            print("✓ Drag and drop successful!")

            # Switch back to main content
            self.driver.switch_to.default_content()

        except Exception as e:
            print(f"✗ Drag and drop demo failed: {e}")
            self.driver.switch_to.default_content()

    def slider_demo(self):
        """
        Demonstrates slider interaction using drag by offset
        Uses: https://jqueryui.com/slider/
        """
        print("\n=== Slider Demo ===")
        self.driver.get("https://jqueryui.com/slider/")

        try:
            # Switch to iframe
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "demo-frame"))
            )
            self.driver.switch_to.frame(iframe)

            # Find slider handle
            slider = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#slider .ui-slider-handle"))
            )

            # Get slider initial position
            initial_position = slider.location['x']
            print(f"Slider initial position: {initial_position}px")

            # Drag slider to the right by 100px
            print("Dragging slider to the right...")
            self.actions.click_and_hold(slider)\
                       .move_by_offset(100, 0)\
                       .release()\
                       .perform()

            # Get new position
            new_position = slider.location['x']
            print(f"Slider new position: {new_position}px")
            print(f"Moved by: {new_position - initial_position}px")
            print("✓ Slider interaction successful!")

            # Switch back
            self.driver.switch_to.default_content()

        except Exception as e:
            print(f"✗ Slider demo failed: {e}")
            self.driver.switch_to.default_content()

    def keyboard_shortcuts_demo(self):
        """
        Demonstrates keyboard shortcuts and key combinations
        Uses: Google search
        """
        print("\n=== Keyboard Shortcuts Demo ===")
        self.driver.get("https://www.google.com")

        try:
            # Find search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            # Type text
            search_text = "ActionChains Selenium Python"
            print(f"Typing: '{search_text}'")
            search_box.send_keys(search_text)

            # Select all with Ctrl+A (Cmd+A on Mac)
            print("Selecting all text (Ctrl+A / Cmd+A)...")
            if sys.platform == "darwin":  # macOS
                self.actions.key_down(Keys.COMMAND)\
                           .send_keys('a')\
                           .key_up(Keys.COMMAND)\
                           .perform()
            else:  # Windows/Linux
                self.actions.key_down(Keys.CONTROL)\
                           .send_keys('a')\
                           .key_up(Keys.CONTROL)\
                           .perform()

            # Type new text (replaces selection)
            new_text = "Selenium Best Practices"
            print(f"Typing new text: '{new_text}'")
            search_box.send_keys(new_text)

            # Submit with Enter key
            print("Submitting with Enter key...")
            search_box.send_keys(Keys.RETURN)

            # Wait for results
            self.wait.until(
                EC.presence_of_element_located((By.ID, "search"))
            )

            print("✓ Keyboard shortcuts demonstration successful!")

        except Exception as e:
            print(f"✗ Keyboard shortcuts demo failed: {e}")

    def context_menu_demo(self):
        """
        Demonstrates right-click context menu
        Uses: https://swisnl.github.io/jQuery-contextMenu/demo.html
        """
        print("\n=== Context Menu (Right-Click) Demo ===")
        self.driver.get("https://swisnl.github.io/jQuery-contextMenu/demo.html")

        try:
            # Wait for the context menu trigger element
            trigger = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".context-menu-one"))
            )

            print("Right-clicking on element...")
            self.actions.context_click(trigger).perform()

            # Wait for context menu to appear
            context_menu = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "context-menu-list"))
            )

            # Get menu items
            menu_items = context_menu.find_elements(By.CSS_SELECTOR, ".context-menu-item")
            print(f"Context menu appeared with {len(menu_items)} items:")
            for item in menu_items[:5]:  # Show first 5 items
                if item.text:
                    print(f"  - {item.text}")

            print("✓ Context menu interaction successful!")

        except Exception as e:
            print(f"✗ Context menu demo failed: {e}")

    def double_click_demo(self):
        """
        Demonstrates double-click action
        Uses: https://api.jquery.com/dblclick/
        """
        print("\n=== Double-Click Demo ===")
        self.driver.get("https://api.jquery.com/dblclick/")

        try:
            # Switch to iframe with example
            iframe = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            self.driver.switch_to.frame(iframe)

            # Find the div element
            div_element = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "div"))
            )

            initial_color = div_element.value_of_css_property("background-color")
            print(f"Initial background color: {initial_color}")

            # Double-click the element
            print("Double-clicking element...")
            self.actions.double_click(div_element).perform()

            # Wait a moment for color change
            import time
            time.sleep(0.5)

            new_color = div_element.value_of_css_property("background-color")
            print(f"New background color: {new_color}")

            if initial_color != new_color:
                print("✓ Double-click changed the color!")
            else:
                print("Color may have changed (check visually)")

            self.driver.switch_to.default_content()

        except Exception as e:
            print(f"✗ Double-click demo failed: {e}")
            self.driver.switch_to.default_content()


def main():
    """Main execution function"""

    print("="*60)
    print("ActionChains Demonstration")
    print("Showing advanced mouse and keyboard interactions")
    print("="*60)

    with managed_driver('chrome', headless=False) as driver:
        # Maximize window for better visibility
        driver.maximize_window()

        page = ActionChainsPage(driver)

        # Run demonstrations
        try:
            # 1. Hover menu navigation
            page.hover_menu_demo()
            input("\nPress Enter to continue to next demo...")

            # 2. Drag and drop
            page.drag_drop_demo()
            input("\nPress Enter to continue to next demo...")

            # 3. Slider interaction
            page.slider_demo()
            input("\nPress Enter to continue to next demo...")

            # 4. Keyboard shortcuts
            page.keyboard_shortcuts_demo()
            input("\nPress Enter to continue to next demo...")

            # 5. Context menu (right-click)
            page.context_menu_demo()
            input("\nPress Enter to continue to next demo...")

            # 6. Double-click
            page.double_click_demo()

            print("\n" + "="*60)
            print("✓ All ActionChains demonstrations completed!")
            print("="*60)

        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user")
        except Exception as e:
            print(f"\n\n✗ Demo failed: {e}")


if __name__ == "__main__":
    main()
