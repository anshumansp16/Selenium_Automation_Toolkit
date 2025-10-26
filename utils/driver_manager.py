"""
WebDriver Manager Utility
Centralized driver setup with best practices
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from contextlib import contextmanager
from typing import Optional


class DriverFactory:
    """Factory class for creating WebDriver instances with best practices"""

    @staticmethod
    def get_chrome_options(headless: bool = False,
                          disable_images: bool = False,
                          window_size: tuple = (1920, 1080)) -> ChromeOptions:
        """
        Configure Chrome options with common settings

        Args:
            headless: Run browser in headless mode
            disable_images: Disable image loading for faster performance
            window_size: Browser window size (width, height)

        Returns:
            Configured ChromeOptions object
        """
        options = ChromeOptions()

        if headless:
            options.add_argument('--headless')

        # Performance & stability options
        options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)

        # Disable unnecessary features
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        if disable_images:
            prefs = {'profile.managed_default_content_settings.images': 2}
            options.add_experimental_option('prefs', prefs)

        return options

    @staticmethod
    def create_chrome_driver(headless: bool = False,
                            disable_images: bool = False,
                            implicit_wait: int = 10) -> webdriver.Chrome:
        """
        Create Chrome WebDriver with automatic driver management

        Args:
            headless: Run in headless mode
            disable_images: Disable image loading
            implicit_wait: Implicit wait timeout in seconds

        Returns:
            Configured Chrome WebDriver instance
        """
        options = DriverFactory.get_chrome_options(headless, disable_images)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(implicit_wait)
        return driver

    @staticmethod
    def create_firefox_driver(headless: bool = False,
                             implicit_wait: int = 10) -> webdriver.Firefox:
        """
        Create Firefox WebDriver with automatic driver management

        Args:
            headless: Run in headless mode
            implicit_wait: Implicit wait timeout in seconds

        Returns:
            Configured Firefox WebDriver instance
        """
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(implicit_wait)
        return driver


@contextmanager
def managed_driver(browser: str = 'chrome',
                   headless: bool = False,
                   **kwargs):
    """
    Context manager for WebDriver - ensures proper cleanup

    Usage:
        with managed_driver('chrome') as driver:
            driver.get('https://example.com')
            # Your automation code here
        # Driver automatically quits when done

    Args:
        browser: Browser type ('chrome' or 'firefox')
        headless: Run in headless mode
        **kwargs: Additional arguments passed to driver creation

    Yields:
        WebDriver instance
    """
    driver = None
    try:
        if browser.lower() == 'chrome':
            driver = DriverFactory.create_chrome_driver(headless=headless, **kwargs)
        elif browser.lower() == 'firefox':
            driver = DriverFactory.create_firefox_driver(headless=headless, **kwargs)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        yield driver
    finally:
        if driver:
            driver.quit()
