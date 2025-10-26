"""
Cookie Clicker Game Automation
Automates the popular Cookie Clicker game with intelligent purchasing strategy
"""

import time
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.driver_manager import managed_driver


class CookieClickerPage:
    """Page Object Model for Cookie Clicker game"""

    # Locators
    LANG_SELECT_EN = (By.ID, "langSelect-EN")
    BIG_COOKIE = (By.ID, "bigCookie")
    COOKIES_COUNT = (By.ID, "cookies")
    ENABLED_PRODUCTS = (By.CSS_SELECTOR, ".product.unlocked.enabled")

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.url = "https://orteil.dashnet.org/cookieclicker/"

    def navigate(self):
        """Navigate to Cookie Clicker"""
        self.driver.get(self.url)
        return self

    def select_language(self):
        """Select English language"""
        lang_button = self.wait.until(
            EC.element_to_be_clickable(self.LANG_SELECT_EN)
        )
        lang_button.click()
        return self

    def wait_for_game_ready(self):
        """Wait for game to fully load"""
        self.wait.until(
            EC.presence_of_element_located(self.BIG_COOKIE)
        )
        # Additional wait for game initialization
        time.sleep(5)
        return self

    def get_cookie_button(self):
        """Get the main cookie button element"""
        return self.driver.find_element(*self.BIG_COOKIE)

    def get_cookies_element(self):
        """Get the cookies counter element"""
        return self.driver.find_element(*self.COOKIES_COUNT)

    def get_cookie_count(self):
        """
        Parse and return current cookie count

        Returns:
            int: Number of cookies, or 0 if parsing fails
        """
        try:
            cookies_text = self.get_cookies_element().text
            # Handle different text formats: "123 cookies" or "123\ncookies"
            cookie_text = cookies_text.split()[0].replace(",", "")
            return int(cookie_text)
        except (ValueError, IndexError) as e:
            print(f"Failed to parse cookie count: {e}")
            return 0

    def click_cookie(self):
        """Click the big cookie"""
        self.get_cookie_button().click()

    def get_purchasable_products(self):
        """Get list of products that can be purchased"""
        return self.driver.find_elements(*self.ENABLED_PRODUCTS)

    def find_most_expensive_product(self, products):
        """
        Find the most expensive purchasable product

        Args:
            products: List of WebElement products

        Returns:
            tuple: (product_element, price) or (None, 0) if none found
        """
        max_price = 0
        most_expensive = None

        for product in products:
            try:
                # Extract price from product text
                text_parts = product.text.split("\n")
                price_text = text_parts[-1].replace(",", "")

                if price_text.isdigit():
                    price = int(price_text)
                    if price > max_price:
                        max_price = price
                        most_expensive = product
            except (ValueError, IndexError):
                continue

        return most_expensive, max_price

    def purchase_upgrade(self, product):
        """Purchase a product upgrade"""
        if product:
            product.click()
            return True
        return False


class CookieClickerBot:
    """Bot to automate Cookie Clicker gameplay"""

    def __init__(self, driver):
        self.page = CookieClickerPage(driver)
        self.purchase_threshold = 10  # Initial threshold
        self.click_count = 0
        self.purchase_count = 0

    def setup(self):
        """Initialize the game"""
        print("Setting up Cookie Clicker...")
        self.page.navigate()
        self.page.select_language()
        self.page.wait_for_game_ready()
        print("Game ready!")

    def run(self, duration_seconds=60):
        """
        Run the bot for specified duration

        Args:
            duration_seconds: How long to run the bot
        """
        print(f"Running bot for {duration_seconds} seconds...")
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            # Click cookie rapidly
            self.page.click_cookie()
            self.click_count += 1

            # Check for purchases every 10 clicks
            if self.click_count % 10 == 0:
                self._try_purchase()

            # Status update every 100 clicks
            if self.click_count % 100 == 0:
                cookies = self.page.get_cookie_count()
                print(f"Clicks: {self.click_count} | Cookies: {cookies:,} | Purchases: {self.purchase_count}")

        # Final statistics
        self._print_statistics()

    def _try_purchase(self):
        """Try to purchase the most expensive available product"""
        cookies = self.page.get_cookie_count()

        # Only check purchases if we have enough cookies
        if cookies >= self.purchase_threshold:
            products = self.page.get_purchasable_products()

            if products:
                most_expensive, price = self.page.find_most_expensive_product(products)

                if most_expensive and price <= cookies:
                    self.page.purchase_upgrade(most_expensive)
                    self.purchase_count += 1
                    # Increase threshold exponentially
                    self.purchase_threshold = max(price * 2, self.purchase_threshold * 1.5)
                    print(f"✓ Purchased upgrade for {price:,} cookies (Total purchases: {self.purchase_count})")

    def _print_statistics(self):
        """Print final bot statistics"""
        final_cookies = self.page.get_cookie_count()
        print("\n" + "="*50)
        print("Cookie Clicker Bot - Final Statistics")
        print("="*50)
        print(f"Total Clicks: {self.click_count:,}")
        print(f"Total Purchases: {self.purchase_count}")
        print(f"Final Cookie Count: {final_cookies:,}")
        print("="*50)


def main():
    """Main execution function"""

    # Configuration
    RUN_DURATION = 60  # Run for 60 seconds
    HEADLESS = False   # Set to True to run without opening browser window

    with managed_driver('chrome', headless=HEADLESS) as driver:
        bot = CookieClickerBot(driver)
        bot.setup()
        bot.run(duration_seconds=RUN_DURATION)


if __name__ == "__main__":
    main()
