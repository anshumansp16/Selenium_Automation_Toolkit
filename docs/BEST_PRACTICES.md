# Selenium Best Practices & Design Patterns

Advanced techniques and patterns for professional browser automation.

## Table of Contents

- [Design Patterns](#design-patterns)
- [Code Organization](#code-organization)
- [Performance Optimization](#performance-optimization)
- [Reliability & Stability](#reliability--stability)
- [Security & Privacy](#security--privacy)
- [Testing Best Practices](#testing-best-practices)
- [Common Pitfalls](#common-pitfalls)

---

## Design Patterns

### Page Object Model (POM)

**Best Practice**: Separate page structure from test logic.

```python
# ❌ Bad: Direct element access in tests
def test_login():
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "submit").click()

# ✅ Good: Page Object Model
class LoginPage:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "submit")

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()
        return DashboardPage(self.driver)

# Usage
def test_login():
    login_page = LoginPage(driver)
    dashboard = login_page.login("user", "pass")
```

**Benefits**:
- Centralized element locators
- Reusable page methods
- Easy maintenance when UI changes
- Better test readability

### Factory Pattern

**Use Case**: Create different driver instances based on configuration.

```python
class DriverFactory:
    @staticmethod
    def create_driver(browser_type, headless=False):
        if browser_type == "chrome":
            return DriverFactory._create_chrome(headless)
        elif browser_type == "firefox":
            return DriverFactory._create_firefox(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")

    @staticmethod
    def _create_chrome(headless):
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Chrome(options=options)
```

### Singleton Pattern

**Use Case**: Single driver instance across test suite.

```python
class DriverSingleton:
    _instance = None
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = DriverFactory.create_driver("chrome")
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
```

**Warning**: Use with caution - can cause test interdependencies.

### Fluent Interface Pattern

**Use Case**: Chain method calls for readable test code.

```python
class FluentPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        self.driver.find_element(By.ID, "username").send_keys(username)
        return self  # Return self for chaining

    def enter_password(self, password):
        self.driver.find_element(By.ID, "password").send_keys(password)
        return self

    def submit(self):
        self.driver.find_element(By.ID, "submit").click()
        return DashboardPage(self.driver)

# Usage - method chaining
page.enter_username("user").enter_password("pass").submit()
```

---

## Code Organization

### Project Structure

```
project/
├── pages/              # Page Objects
│   ├── __init__.py
│   ├── base_page.py   # Base class
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/              # Test files
│   ├── __init__.py
│   ├── test_login.py
│   └── test_dashboard.py
├── utils/              # Utilities
│   ├── __init__.py
│   ├── driver_manager.py
│   └── helpers.py
├── config/             # Configuration
│   ├── __init__.py
│   └── settings.py
└── requirements.txt
```

### Base Page Class

```python
class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator):
        """Find single element with wait"""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        """Find multiple elements"""
        self.wait.until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """Click element when clickable"""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type(self, locator, text):
        """Clear and type text"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get element text"""
        return self.find_element(locator).text

    def is_visible(self, locator, timeout=None):
        """Check if element is visible"""
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator):
        """Wait for element to become invisible"""
        self.wait.until(
            EC.invisibility_of_element_located(locator)
        )

    def scroll_to_element(self, locator):
        """Scroll element into view"""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            element
        )
```

### Configuration Management

```python
# config/settings.py
import os

class Config:
    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))

    # URLs
    BASE_URL = os.getenv("BASE_URL", "https://example.com")

    # Timeouts
    DEFAULT_TIMEOUT = 10
    LONG_TIMEOUT = 30

    # Screenshots
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "screenshots"

# Usage
from config.settings import Config

driver.get(Config.BASE_URL)
```

---

## Performance Optimization

### 1. Disable Unnecessary Browser Features

```python
options = ChromeOptions()

# Disable images for faster loading
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# Disable CSS (if not needed for testing)
prefs["profile.default_content_setting_values"]["stylesheet"] = 2

# Disable JavaScript (only if your app doesn't need it)
prefs["profile.managed_default_content_settings.javascript"] = 2

options.add_experimental_option("prefs", prefs)
```

### 2. Use Appropriate Waits

```python
# ❌ Bad: Fixed sleep wastes time
time.sleep(5)  # Always waits 5 seconds

# ✅ Good: Dynamic wait only as long as needed
wait.until(EC.presence_of_element_located(locator))  # Proceeds as soon as element appears
```

### 3. Minimize Driver Initialization

```python
# ❌ Bad: Create new driver for each test
def test_1():
    driver = webdriver.Chrome()
    # ...
    driver.quit()

def test_2():
    driver = webdriver.Chrome()  # Slow!
    # ...
    driver.quit()

# ✅ Good: Reuse driver across tests
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
```

### 4. Use Headless Mode for CI/CD

```python
# Headless mode is faster and doesn't require display
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
```

### 5. Optimize Locator Strategy

```python
# ❌ Slow: XPath with complex traversal
driver.find_element(By.XPATH, "//div[@class='container']/descendant::button[@id='submit']")

# ✅ Fast: Direct CSS selector
driver.find_element(By.CSS_SELECTOR, "#submit")
```

### 6. Batch Operations

```python
# ❌ Bad: Multiple separate calls
driver.find_element(By.ID, "field1").send_keys("text1")
driver.find_element(By.ID, "field2").send_keys("text2")
driver.find_element(By.ID, "field3").send_keys("text3")

# ✅ Good: Find all at once and iterate
fields = {
    "field1": "text1",
    "field2": "text2",
    "field3": "text3"
}
for field_id, text in fields.items():
    driver.find_element(By.ID, field_id).send_keys(text)
```

---

## Reliability & Stability

### 1. Handle Stale Element References

```python
def click_with_retry(driver, locator, max_attempts=3):
    """Click element with automatic retry on stale element"""
    for attempt in range(max_attempts):
        try:
            element = driver.find_element(*locator)
            element.click()
            return
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(0.5)
```

### 2. Wait for AJAX/Dynamic Content

```python
def wait_for_ajax(driver, timeout=10):
    """Wait for jQuery AJAX calls to complete"""
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.execute_script("return jQuery.active == 0"))

def wait_for_page_load(driver, timeout=10):
    """Wait for page to fully load"""
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
```

### 3. Robust Element Interaction

```python
def safe_click(driver, locator, timeout=10):
    """Click element with multiple fallback strategies"""
    wait = WebDriverWait(driver, timeout)

    try:
        # Strategy 1: Standard click
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    except ElementClickInterceptedException:
        # Strategy 2: JavaScript click
        element = driver.find_element(*locator)
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        # Strategy 3: Action chains
        element = driver.find_element(*locator)
        ActionChains(driver).move_to_element(element).click().perform()
```

### 4. Handle Flaky Tests

```python
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_flaky_scenario():
    """Test will retry up to 3 times on failure"""
    pass
```

### 5. Implement Custom Expected Conditions

```python
class element_has_class:
    """Custom expected condition to check if element has specific class"""

    def __init__(self, locator, class_name):
        self.locator = locator
        self.class_name = class_name

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        classes = element.get_attribute("class")
        return self.class_name in classes.split()

# Usage
wait.until(element_has_class((By.ID, "button"), "active"))
```

---

## Security & Privacy

### 1. Avoid Hardcoding Credentials

```python
# ❌ Bad: Credentials in code
username = "admin"
password = "secret123"

# ✅ Good: Use environment variables
import os
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

# ✅ Better: Use secrets manager
from config.secrets import get_credential
username = get_credential("TEST_USERNAME")
```

### 2. Clean Up Sensitive Data

```python
def test_with_cleanup():
    try:
        # Test logic
        login(username, password)
    finally:
        # Always clean up
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
```

### 3. Use Incognito/Private Mode

```python
options = ChromeOptions()
options.add_argument("--incognito")

# Or for Firefox
options = FirefoxOptions()
options.add_argument("-private")
```

---

## Testing Best Practices

### 1. Test Independence

```python
# ❌ Bad: Tests depend on each other
def test_create_user():
    # Creates user
    global user_id
    user_id = create_user()

def test_update_user():
    # Depends on test_create_user
    update_user(user_id)  # Fails if test_create_user fails

# ✅ Good: Each test is independent
def test_create_user():
    user_id = create_user()
    assert user_id is not None

def test_update_user():
    # Create its own test data
    user_id = create_user()
    result = update_user(user_id)
    assert result.success
```

### 2. Data-Driven Testing

```python
import pytest

@pytest.mark.parametrize("username,password,expected", [
    ("valid_user", "valid_pass", "success"),
    ("invalid_user", "wrong_pass", "error"),
    ("", "", "error"),
])
def test_login_scenarios(username, password, expected):
    result = login_page.login(username, password)
    assert result.status == expected
```

### 3. Fixtures for Setup/Teardown

```python
@pytest.fixture
def authenticated_session(driver):
    """Fixture that provides authenticated session"""
    login_page = LoginPage(driver)
    login_page.login("test_user", "test_pass")
    yield driver
    # Teardown
    driver.delete_all_cookies()

def test_dashboard(authenticated_session):
    # Test starts with authenticated session
    dashboard = DashboardPage(authenticated_session)
    assert dashboard.is_loaded()
```

### 4. Screenshot on Failure

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Take screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_name = f"failure_{item.name}.png"
            driver.save_screenshot(screenshot_name)
            print(f"Screenshot saved: {screenshot_name}")
```

---

## Common Pitfalls

### 1. Not Using Explicit Waits

```python
# ❌ Pitfall: Race conditions
driver.find_element(By.ID, "button").click()  # May fail if element not ready

# ✅ Solution
wait.until(EC.element_to_be_clickable((By.ID, "button"))).click()
```

### 2. Using Time.sleep()

```python
# ❌ Pitfall: Wastes time, unreliable
time.sleep(3)

# ✅ Solution
wait.until(EC.presence_of_element_located(locator))
```

### 3. Not Closing Driver

```python
# ❌ Pitfall: Resource leak
driver = webdriver.Chrome()
# ... test code ...
# Forgot driver.quit()

# ✅ Solution: Use context manager
with managed_driver() as driver:
    # ... test code ...
# Automatically calls quit()
```

### 4. Brittle Locators

```python
# ❌ Pitfall: XPath based on position (breaks easily)
driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/button[1]")

# ✅ Solution: Use meaningful attributes
driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-button']")
```

### 5. Not Handling Exceptions

```python
# ❌ Pitfall: Unhandled exceptions crash tests
element = driver.find_element(By.ID, "optional-element")

# ✅ Solution
try:
    element = driver.find_element(By.ID, "optional-element")
except NoSuchElementException:
    element = None
```

### 6. Testing Too Much in One Test

```python
# ❌ Pitfall: Long test that does everything
def test_entire_user_journey():
    test_registration()
    test_login()
    test_profile_update()
    test_purchase()
    test_logout()  # If this fails, hard to debug

# ✅ Solution: Split into separate tests
def test_registration():
    # ...

def test_login():
    # ...
```

---

## Advanced Techniques

### Parallel Test Execution

```python
# Using pytest-xdist
# Install: pip install pytest-xdist

# Run tests in parallel (4 workers)
# pytest -n 4
```

### Browser Console Logs

```python
# Capture browser console errors
logs = driver.get_log('browser')
errors = [log for log in logs if log['level'] == 'SEVERE']
assert len(errors) == 0, f"Console errors: {errors}"
```

### Network Interception (Chrome DevTools Protocol)

```python
# Monitor network requests
driver.execute_cdp_cmd('Network.enable', {})

# Get network logs
logs = driver.get_log('performance')
```

### Mobile Emulation

```python
mobile_emulation = {
    "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
}
options = ChromeOptions()
options.add_experimental_option("mobileEmulation", mobile_emulation)
```

---

## Summary

**Golden Rules**:
1. Use Page Object Model
2. Never use `time.sleep()`
3. Always use explicit waits
4. Handle exceptions gracefully
5. Keep tests independent
6. Use meaningful locators
7. Clean up resources
8. Optimize for performance
9. Secure sensitive data
10. Make tests maintainable

**For quick reference, see [SELENIUM_GUIDE.md](SELENIUM_GUIDE.md)**
