# Selenium Quick Reference Guide

Essential Selenium commands and patterns for browser automation.

## Table of Contents

- [Locators](#locators)
- [Waits](#waits)
- [Element Interactions](#element-interactions)
- [ActionChains - Advanced Interactions](#actionchains---advanced-interactions)
- [Browser Operations](#browser-operations)
- [Remote WebDriver](#remote-webdriver)
- [Advanced Techniques](#advanced-techniques)

---

## Locators

### Locator Types (Priority Order)

Use locators in this priority for best performance and reliability:

1. **ID** - Fastest and most reliable
2. **Name** - Good for form elements
3. **CSS Selector** - Flexible and fast
4. **XPath** - Most powerful but slowest

```python
from selenium.webdriver.common.by import By

# ID (Best - Unique and fast)
element = driver.find_element(By.ID, "submit-button")

# Name (Good for forms)
element = driver.find_element(By.NAME, "username")

# Class Name
element = driver.find_element(By.CLASS_NAME, "btn-primary")

# CSS Selector (Recommended for complex queries)
element = driver.find_element(By.CSS_SELECTOR, "div.container > button#submit")

# XPath (Use when CSS can't do it)
element = driver.find_element(By.XPATH, "//button[@id='submit']")

# Tag Name
element = driver.find_element(By.TAG_NAME, "h1")

# Link Text (Exact match)
element = driver.find_element(By.LINK_TEXT, "Click Here")

# Partial Link Text
element = driver.find_element(By.PARTIAL_LINK_TEXT, "Click")
```

### CSS Selector Cheat Sheet

```python
# By attribute
driver.find_element(By.CSS_SELECTOR, "[data-test='login']")

# By multiple attributes
driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='username']")

# Direct child
driver.find_element(By.CSS_SELECTOR, "div.parent > button")

# Descendant
driver.find_element(By.CSS_SELECTOR, "div.parent button")

# By position
driver.find_element(By.CSS_SELECTOR, "ul > li:nth-child(2)")
driver.find_element(By.CSS_SELECTOR, "ul > li:first-child")
driver.find_element(By.CSS_SELECTOR, "ul > li:last-child")

# Contains class
driver.find_element(By.CSS_SELECTOR, "button.btn.active")

# Contains text (not direct support, use XPath)
```

### XPath Essentials

```python
# Basic path
driver.find_element(By.XPATH, "//div[@id='main']")

# Contains text
driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")

# Multiple attributes
driver.find_element(By.XPATH, "//input[@type='text' and @name='email']")

# Parent selection
driver.find_element(By.XPATH, "//span[@class='price']/parent::div")

# Following sibling
driver.find_element(By.XPATH, "//label[@for='username']/following-sibling::input")

# Ancestor
driver.find_element(By.XPATH, "//button[@id='submit']/ancestor::form")

# Contains attribute
driver.find_element(By.XPATH, "//a[contains(@href, 'login')]")
```

---

## Waits

**NEVER use `time.sleep()`!** Use Selenium waits instead.

### Implicit Wait

Sets a default wait time for all `find_element` calls:

```python
# Set once at the beginning
driver.implicitly_wait(10)  # Wait up to 10 seconds
```

### Explicit Wait (Recommended)

Wait for specific conditions:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

# Wait for element to be present
element = wait.until(
    EC.presence_of_element_located((By.ID, "submit"))
)

# Wait for element to be clickable
element = wait.until(
    EC.element_to_be_clickable((By.ID, "submit"))
)

# Wait for element to be visible
element = wait.until(
    EC.visibility_of_element_located((By.ID, "result"))
)

# Wait for text to be present
wait.until(
    EC.text_to_be_present_in_element((By.ID, "status"), "Complete")
)

# Wait for element to disappear
wait.until(
    EC.invisibility_of_element_located((By.ID, "loading"))
)
```

### Common Expected Conditions

```python
# Element conditions
EC.presence_of_element_located(locator)
EC.visibility_of_element_located(locator)
EC.element_to_be_clickable(locator)
EC.element_to_be_selected(locator)

# Text conditions
EC.text_to_be_present_in_element(locator, text)
EC.text_to_be_present_in_element_value(locator, text)

# Alert conditions
EC.alert_is_present()

# Title conditions
EC.title_is(title)
EC.title_contains(title)

# URL conditions
EC.url_contains(url_part)
EC.url_to_be(url)

# Frame conditions
EC.frame_to_be_available_and_switch_to_it(locator)

# Invisibility
EC.invisibility_of_element_located(locator)
EC.staleness_of(element)
```

### Custom Wait Conditions

```python
# Wait with custom condition
wait.until(lambda driver: driver.find_element(By.ID, "result").text != "")

# Wait with timeout handling
from selenium.common.exceptions import TimeoutException

try:
    element = wait.until(EC.presence_of_element_located((By.ID, "result")))
except TimeoutException:
    print("Element not found within timeout period")
```

---

## Element Interactions

### Basic Actions

```python
# Click
element.click()

# Send text
element.send_keys("Hello World")

# Clear text field
element.clear()

# Submit form
element.submit()

# Get text
text = element.text

# Get attribute
value = element.get_attribute("value")
href = element.get_attribute("href")

# Get CSS property
color = element.value_of_css_property("color")

# Check if element is displayed/enabled/selected
is_visible = element.is_displayed()
is_enabled = element.is_enabled()
is_checked = element.is_selected()
```

### Dropdown/Select Elements

```python
from selenium.webdriver.support.ui import Select

select_element = driver.find_element(By.ID, "country")
select = Select(select_element)

# Select by visible text
select.select_by_visible_text("United States")

# Select by value attribute
select.select_by_value("us")

# Select by index (0-based)
select.select_by_index(1)

# Get selected option
selected = select.first_selected_option.text

# Get all options
all_options = select.options

# Deselect (multi-select only)
select.deselect_all()
select.deselect_by_visible_text("Option 1")
```

### Keyboard Actions

```python
from selenium.webdriver.common.keys import Keys

# Special keys
element.send_keys(Keys.RETURN)      # Enter
element.send_keys(Keys.TAB)         # Tab
element.send_keys(Keys.ESCAPE)      # Escape
element.send_keys(Keys.BACKSPACE)   # Backspace
element.send_keys(Keys.DELETE)      # Delete
element.send_keys(Keys.SPACE)       # Space

# Arrow keys
element.send_keys(Keys.ARROW_DOWN)
element.send_keys(Keys.ARROW_UP)
element.send_keys(Keys.ARROW_LEFT)
element.send_keys(Keys.ARROW_RIGHT)

# Key combinations
element.send_keys(Keys.CONTROL, 'a')  # Ctrl+A (Select all)
element.send_keys(Keys.CONTROL, 'c')  # Ctrl+C (Copy)

# On Mac, use COMMAND instead of CONTROL
element.send_keys(Keys.COMMAND, 'a')
```

---

## ActionChains - Advanced Interactions

ActionChains provide a way to automate low-level interactions like mouse movements, keyboard actions, and complex gestures. All actions are stored in a queue and executed when `perform()` is called.

### Basic Usage Pattern

```python
from selenium.webdriver.common.action_chains import ActionChains

# Create ActionChains instance
actions = ActionChains(driver)

# Chain actions together
actions.move_to_element(element).click().perform()
```

### Mouse Actions

```python
from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)
element = driver.find_element(By.ID, "menu")

# Hover over element (move_to_element)
actions.move_to_element(element).perform()

# Click element
actions.click(element).perform()

# Click without moving to element first
actions.click().perform()  # Clicks at current mouse position

# Double click
actions.double_click(element).perform()

# Right click (context click)
actions.context_click(element).perform()

# Click and hold
actions.click_and_hold(element).perform()

# Release mouse button
actions.release(element).perform()

# Move to element with offset
actions.move_to_element_with_offset(element, xoffset=10, yoffset=20).perform()

# Move by offset from current position
actions.move_by_offset(100, 50).perform()
```

### Drag and Drop

```python
source = driver.find_element(By.ID, "source")
target = driver.find_element(By.ID, "target")

# Method 1: drag_and_drop
actions.drag_and_drop(source, target).perform()

# Method 2: Manual drag and drop
actions.click_and_hold(source).move_to_element(target).release().perform()

# Method 3: Drag by offset
actions.drag_and_drop_by_offset(source, xoffset=100, yoffset=50).perform()

# Method 4: Complex drag with pause
actions.click_and_hold(source)\
       .pause(0.5)\
       .move_to_element(target)\
       .pause(0.5)\
       .release()\
       .perform()
```

### Keyboard Actions with ActionChains

```python
from selenium.webdriver.common.keys import Keys

# Send keys to element
element = driver.find_element(By.ID, "input")
actions.send_keys_to_element(element, "Hello World").perform()

# Send keys to currently focused element
actions.send_keys("Hello").perform()

# Key combinations
actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()  # Ctrl+A

# Multiple key combinations
actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('T').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()

# Hold and release individual keys
actions.key_down(Keys.SHIFT).send_keys("hello").key_up(Keys.SHIFT).perform()  # Sends "HELLO"
```

### Complex Action Chains

```python
# Example 1: Hover menu navigation
menu = driver.find_element(By.ID, "menu")
submenu = driver.find_element(By.ID, "submenu")
item = driver.find_element(By.ID, "item")

actions.move_to_element(menu)\
       .pause(1)\
       .move_to_element(submenu)\
       .pause(1)\
       .click(item)\
       .perform()

# Example 2: Drawing with mouse (signature pad)
canvas = driver.find_element(By.ID, "canvas")
actions.move_to_element(canvas)\
       .click_and_hold()\
       .move_by_offset(50, 0)\
       .move_by_offset(0, 50)\
       .move_by_offset(-50, 0)\
       .move_by_offset(0, -50)\
       .release()\
       .perform()

# Example 3: Multi-select with Ctrl
first_item = driver.find_element(By.ID, "item1")
second_item = driver.find_element(By.ID, "item2")

actions.click(first_item)\
       .key_down(Keys.CONTROL)\
       .click(second_item)\
       .key_up(Keys.CONTROL)\
       .perform()
```

### Pause Between Actions

```python
# Add delay between actions (in seconds)
actions.move_to_element(element1)\
       .pause(1)\
       .click()\
       .pause(0.5)\
       .move_to_element(element2)\
       .perform()
```

### Resetting Action Chains

```python
# Reset all actions in the queue
actions.reset_actions()

# Or create a new instance
actions = ActionChains(driver)
```

### Scrolling with ActionChains

```python
# Scroll to element
element = driver.find_element(By.ID, "footer")
actions.scroll_to_element(element).perform()

# Scroll by amount
actions.scroll_by_amount(0, 500).perform()  # Scroll down 500px

# Scroll from element
actions.scroll_from_origin(
    ScrollOrigin.from_element(element),
    0,
    100
).perform()
```

### Common Use Cases

```python
# Slider interaction
slider = driver.find_element(By.ID, "slider")
actions.click_and_hold(slider).move_by_offset(50, 0).release().perform()

# Tooltip hover
element = driver.find_element(By.ID, "info-icon")
actions.move_to_element(element).perform()
tooltip_text = driver.find_element(By.CLASS_NAME, "tooltip").text

# Copy and paste
text_field = driver.find_element(By.ID, "text")
actions.click(text_field)\
       .key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)\
       .key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL)\
       .perform()

# Right-click context menu
actions.context_click(element).perform()
context_menu_item = driver.find_element(By.ID, "delete")
context_menu_item.click()
```

### Important Notes

- **Always call `perform()`** - Actions are queued until `perform()` is called
- **Actions execute in order** - They run sequentially as chained
- **Use `pause()`** - For timing-sensitive interactions instead of `time.sleep()`
- **Reset when needed** - Clear action queue with `reset_actions()`
- **Handle stale elements** - Re-find elements if they change during action execution

---

## Browser Operations

### Navigation

```python
# Open URL
driver.get("https://example.com")

# Refresh page
driver.refresh()

# Back
driver.back()

# Forward
driver.forward()

# Get current URL
current_url = driver.current_url

# Get page title
title = driver.title

# Get page source
html = driver.page_source
```

### Windows & Tabs

```python
# Open new tab
driver.execute_script("window.open('');")

# Get all window handles
windows = driver.window_handles

# Switch to window by index
driver.switch_to.window(windows[1])

# Switch to original window
driver.switch_to.window(windows[0])

# Close current window
driver.close()

# Close all windows and quit
driver.quit()

# Get window size
size = driver.get_window_size()

# Set window size
driver.set_window_size(1920, 1080)

# Maximize window
driver.maximize_window()

# Minimize window
driver.minimize_window()

# Fullscreen
driver.fullscreen_window()
```

### Frames & iFrames

```python
# Switch to frame by index
driver.switch_to.frame(0)

# Switch to frame by name/ID
driver.switch_to.frame("frameName")

# Switch to frame by WebElement
iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)

# Switch back to main content
driver.switch_to.default_content()

# Switch to parent frame
driver.switch_to.parent_frame()
```

### Alerts & Popups

```python
from selenium.webdriver.support import expected_conditions as EC

# Wait for alert
wait.until(EC.alert_is_present())

# Switch to alert
alert = driver.switch_to.alert

# Get alert text
text = alert.text

# Accept alert (click OK)
alert.accept()

# Dismiss alert (click Cancel)
alert.dismiss()

# Send text to prompt
alert.send_keys("Hello")
```

### Screenshots

```python
# Full page screenshot
driver.save_screenshot("screenshot.png")

# Element screenshot
element = driver.find_element(By.ID, "content")
element.screenshot("element.png")

# Get screenshot as bytes
screenshot_bytes = driver.get_screenshot_as_png()

# Get screenshot as base64
screenshot_base64 = driver.get_screenshot_as_base64()
```

### JavaScript Execution

```python
# Execute JavaScript
driver.execute_script("console.log('Hello');")

# Return value from JavaScript
result = driver.execute_script("return document.title;")

# Scroll to element
element = driver.find_element(By.ID, "footer")
driver.execute_script("arguments[0].scrollIntoView();", element)

# Click using JavaScript (bypass visibility checks)
driver.execute_script("arguments[0].click();", element)

# Set attribute value
driver.execute_script("arguments[0].setAttribute('value', 'new value');", element)
```

---

## Remote WebDriver

Remote WebDriver allows you to run Selenium tests on a different machine or in containerized environments. This is essential for distributed testing, cloud testing services, and CI/CD pipelines.

### Basic Remote WebDriver Setup

```python
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Connect to remote Selenium server
driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME
)

driver.get('https://example.com')
driver.quit()
```

### Selenium Grid Setup

```python
# Chrome on remote grid
driver = webdriver.Remote(
    command_executor='http://selenium-hub:4444/wd/hub',
    options=webdriver.ChromeOptions()
)

# Firefox on remote grid
driver = webdriver.Remote(
    command_executor='http://selenium-hub:4444/wd/hub',
    options=webdriver.FirefoxOptions()
)
```

### Using Options with Remote WebDriver

```python
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Configure Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Create remote driver with options
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)
```

### Platform and Browser Selection

```python
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Specify platform
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['platform'] = 'LINUX'
capabilities['version'] = '120.0'

driver = webdriver.Remote(
    command_executor='http://hub-url:4444/wd/hub',
    desired_capabilities=capabilities
)
```

### Cloud Testing Services

#### BrowserStack

```python
from selenium.webdriver.chrome.options import Options

capabilities = {
    'browserName': 'Chrome',
    'browserVersion': '120.0',
    'bstack:options': {
        'os': 'Windows',
        'osVersion': '11',
        'sessionName': 'My Test',
        'userName': 'YOUR_USERNAME',
        'accessKey': 'YOUR_ACCESS_KEY'
    }
}

driver = webdriver.Remote(
    command_executor='https://hub.browserstack.com/wd/hub',
    desired_capabilities=capabilities
)
```

#### Sauce Labs

```python
sauce_options = {
    'username': 'YOUR_USERNAME',
    'accessKey': 'YOUR_ACCESS_KEY',
    'browserName': 'chrome',
    'browserVersion': 'latest',
    'platformName': 'Windows 11'
}

driver = webdriver.Remote(
    command_executor='https://ondemand.saucelabs.com:443/wd/hub',
    options=sauce_options
)
```

#### LambdaTest

```python
lt_options = {
    'user': 'YOUR_USERNAME',
    'accessKey': 'YOUR_ACCESS_KEY',
    'build': 'Test Build',
    'name': 'Test Name',
    'platformName': 'Windows 11',
    'browserName': 'Chrome',
    'browserVersion': 'latest'
}

driver = webdriver.Remote(
    command_executor='https://hub.lambdatest.com/wd/hub',
    options=lt_options
)
```

### Docker + Selenium Grid

#### Using Standalone Chrome Container

```bash
# Run Selenium Chrome container
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:latest
```

```python
# Connect to Docker container
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=webdriver.ChromeOptions()
)
```

#### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3'
services:
  selenium-hub:
    image: selenium/hub:latest
    ports:
      - "4444:4444"

  chrome:
    image: selenium/node-chrome:latest
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
```

```python
# Connect to Docker Compose grid
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=webdriver.ChromeOptions()
)
```

### Appium (Mobile Testing)

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options

# Android setup
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'Android Emulator'
options.app = '/path/to/app.apk'
options.automation_name = 'UiAutomator2'

driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723',
    options=options
)

# iOS setup
from appium.options.ios import XCUITestOptions

ios_options = XCUITestOptions()
ios_options.platform_name = 'iOS'
ios_options.device_name = 'iPhone 14'
ios_options.app = '/path/to/app.app'
ios_options.automation_name = 'XCUITest'

driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723',
    options=ios_options
)
```

### Remote WebDriver with Context Manager

```python
from contextlib import contextmanager

@contextmanager
def remote_driver(hub_url, browser='chrome'):
    """Context manager for remote WebDriver"""
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()

    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options
    )

    try:
        yield driver
    finally:
        driver.quit()

# Usage
with remote_driver('http://localhost:4444/wd/hub', 'chrome') as driver:
    driver.get('https://example.com')
    # Your test code here
```

### Debugging Remote Sessions

```python
# Enable logging
import logging

logging.basicConfig(level=logging.DEBUG)

# Get session info
session_id = driver.session_id
print(f"Session ID: {session_id}")

# Get capabilities
capabilities = driver.capabilities
print(f"Capabilities: {capabilities}")

# Check if remote
print(f"Is remote: {driver.command_executor._url}")
```

### File Upload with Remote WebDriver

```python
# For remote WebDriver, use file detector
from selenium.webdriver.remote.file_detector import LocalFileDetector

driver.file_detector = LocalFileDetector()

# Now file upload works with local paths
file_input = driver.find_element(By.ID, "upload")
file_input.send_keys("/local/path/to/file.pdf")
```

### Best Practices for Remote WebDriver

```python
# 1. Use environment variables for credentials
import os

HUB_URL = os.getenv('SELENIUM_HUB_URL', 'http://localhost:4444/wd/hub')
USERNAME = os.getenv('SELENIUM_USERNAME')
ACCESS_KEY = os.getenv('SELENIUM_ACCESS_KEY')

# 2. Set timeouts
driver.set_page_load_timeout(30)
driver.set_script_timeout(30)

# 3. Handle network issues
from selenium.common.exceptions import WebDriverException

try:
    driver = webdriver.Remote(
        command_executor=HUB_URL,
        options=chrome_options
    )
except WebDriverException as e:
    print(f"Failed to connect to remote hub: {e}")
    raise

# 4. Clean up properly
try:
    # Your test code
    pass
finally:
    driver.quit()
```

### Parallel Testing with Remote WebDriver

```python
import concurrent.futures
from selenium import webdriver

def run_test(browser):
    """Run test on specific browser"""
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    try:
        driver.get('https://example.com')
        # Your test logic
        return f"{browser}: Success"
    finally:
        driver.quit()

# Run tests in parallel
browsers = ['chrome', 'firefox', 'chrome', 'firefox']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(run_test, browsers)

for result in results:
    print(result)
```

### Key Differences: Local vs Remote

| Feature | Local WebDriver | Remote WebDriver |
|---------|----------------|------------------|
| Driver Location | Same machine | Different machine/container |
| Setup | Direct driver instance | Connect to hub URL |
| File Upload | Direct path works | Need `LocalFileDetector` |
| Performance | Faster | Network latency |
| Scalability | Limited | Highly scalable |
| Use Case | Development | CI/CD, Grid testing |

---

## Advanced Techniques

### Cookies

```python
# Get all cookies
cookies = driver.get_cookies()

# Get specific cookie
cookie = driver.get_cookie("session_id")

# Add cookie
driver.add_cookie({"name": "test", "value": "123"})

# Delete cookie
driver.delete_cookie("session_id")

# Delete all cookies
driver.delete_all_cookies()
```

### File Upload

```python
# Simple upload (send file path to input)
file_input = driver.find_element(By.ID, "fileUpload")
file_input.send_keys("/absolute/path/to/file.pdf")

# For hidden inputs, use JavaScript
driver.execute_script(
    "arguments[0].style.display = 'block';",
    file_input
)
```

### Handling Multiple Elements

```python
# Find all matching elements
elements = driver.find_elements(By.CLASS_NAME, "item")

# Iterate over elements
for element in elements:
    print(element.text)

# Filter elements
enabled_buttons = [e for e in elements if e.is_enabled()]

# Get count
count = len(elements)
```

### Error Handling

```python
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

try:
    element = driver.find_element(By.ID, "button")
    element.click()
except NoSuchElementException:
    print("Element not found")
except TimeoutException:
    print("Operation timed out")
except StaleElementReferenceException:
    # Element changed, refind it
    element = driver.find_element(By.ID, "button")
except ElementClickInterceptedException:
    # Something is covering the element
    driver.execute_script("arguments[0].click();", element)
```

### Checking Element Existence

```python
# Method 1: Try-except
def element_exists(driver, locator):
    try:
        driver.find_element(*locator)
        return True
    except NoSuchElementException:
        return False

# Method 2: Using find_elements (no exception)
def element_exists_v2(driver, locator):
    return len(driver.find_elements(*locator)) > 0

# Usage
if element_exists(driver, (By.ID, "optional-element")):
    print("Element exists!")
```

---

## Quick Tips

1. **Always use waits** - Avoid `time.sleep()`
2. **Prefer CSS over XPath** - Faster and more readable
3. **Use Page Object Model** - Better code organization
4. **Close resources** - Always call `driver.quit()`
5. **Handle exceptions** - Gracefully handle errors
6. **Use unique locators** - ID is best, then CSS
7. **Keep it DRY** - Reuse common methods
8. **Log strategically** - Debug issues faster

---

**For more advanced patterns, see [BEST_PRACTICES.md](BEST_PRACTICES.md)**
