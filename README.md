# Selenium Automation Toolkit

Professional Selenium browser automation framework with best practices, reusable templates, and practical examples.

## Features

- **Automatic WebDriver Management**: No manual ChromeDriver downloads needed
- **Page Object Model**: Clean, maintainable code structure
- **Production-Ready Templates**: Boilerplate code to start new projects instantly
- **Practical Examples**: Real-world automation scenarios
- **Best Practices**: Modern Selenium patterns (2025)

## Quick Start

### Installation

```bash
# Clone or navigate to this repository
cd selenium-automation-toolkit

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: You do NOT need to manually download ChromeDriver! The `webdriver-manager` package handles this automatically.

### Run Examples

```bash
# Cookie Clicker automation (Game bot with POM)
python examples/cookie_clicker.py

# Form automation (Google search demo)
python examples/form_automation.py

# ActionChains demo (Drag & drop, hover, keyboard shortcuts)
python examples/actionchains_demo.py

# Windows, frames & alerts demo (Multi-window, iframe switching, alerts)
python examples/windows_frames_alerts.py

# Advanced features (JavaScript, screenshots, cookies, local storage)
python examples/advanced_features.py
```

### Start New Project

```bash
# Copy the boilerplate template
cp templates/base_automation.py my_automation.py

# Edit my_automation.py with your automation logic
```

## Project Structure

```
selenium-automation-toolkit/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── docs/
│   ├── SELENIUM_GUIDE.md      # Quick reference for Selenium
│   └── BEST_PRACTICES.md      # Design patterns & advanced topics
├── templates/
│   └── base_automation.py     # Boilerplate code (copy this!)
├── examples/
│   ├── cookie_clicker.py      # Game automation example
│   ├── form_automation.py     # Form interaction examples
│   ├── actionchains_demo.py   # ActionChains: drag/drop, hover, keyboard
│   ├── windows_frames_alerts.py # Windows, iframes, alerts handling
│   └── advanced_features.py   # JavaScript, screenshots, cookies
└── utils/
    ├── driver_manager.py      # WebDriver factory & utilities
    └── __init__.py
```

## Example Scripts

Each example demonstrates different Selenium concepts with real-world scenarios:

| Script | Demonstrates | Key Concepts |
|--------|--------------|--------------|
| **cookie_clicker.py** | Automated game playing | Page Object Model, intelligent strategy, statistics tracking |
| **form_automation.py** | Form interactions | Text input, dropdowns, checkboxes, radio buttons, file upload |
| **actionchains_demo.py** | Advanced interactions | Hover menus, drag & drop, sliders, keyboard shortcuts, context menus |
| **windows_frames_alerts.py** | Window management | Multiple windows/tabs, iframe switching, alerts/confirms/prompts |
| **advanced_features.py** | Advanced techniques | JavaScript execution, screenshots, cookies, local storage, scrolling |

**Interactive Demos**: All examples include step-by-step demonstrations with pauses, making them perfect for learning!

## Basic Usage

### Simple Example

```python
from utils.driver_manager import managed_driver

# Context manager ensures automatic cleanup
with managed_driver('chrome') as driver:
    driver.get('https://example.com')
    print(driver.title)
```

### Using Page Object Model

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_manager import managed_driver

class GooglePage:
    SEARCH_BOX = (By.NAME, "q")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search(self, query):
        search_box = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_BOX)
        )
        search_box.send_keys(query)
        search_box.submit()

# Usage
with managed_driver('chrome') as driver:
    driver.get('https://google.com')
    page = GooglePage(driver)
    page.search('Selenium Python')
```

## Common Use Cases

### Headless Mode (No Browser Window)

```python
with managed_driver('chrome', headless=True) as driver:
    driver.get('https://example.com')
```

### Disable Images (Faster Loading)

```python
from utils.driver_manager import DriverFactory

driver = DriverFactory.create_chrome_driver(
    headless=False,
    disable_images=True
)
```

### Screenshots

```python
driver.save_screenshot('screenshot.png')
```

## Documentation

- **[Selenium Guide](docs/SELENIUM_GUIDE.md)** - Quick reference for locators, waits, and common operations
- **[Best Practices](docs/BEST_PRACTICES.md)** - Design patterns, advanced techniques, and tips

## Configuration

### Chrome Options

Customize browser behavior in `utils/driver_manager.py`:

- Window size
- User agent
- Extensions
- Download directory
- Proxy settings

See `DriverFactory.get_chrome_options()` for available options.

## Troubleshooting

### Common Issues

**Issue**: `ChromeDriver version mismatch`
**Solution**: Delete cached drivers and rerun. `webdriver-manager` will auto-download the correct version.

**Issue**: `Element not found`
**Solution**: Increase wait timeout or use explicit waits (see Selenium Guide).

**Issue**: `Permission denied`
**Solution**: Ensure Chrome is installed and accessible.

## Requirements

- Python 3.8+
- Chrome browser installed
- Internet connection (for automatic driver downloads)

## Contributing

This is a personal toolkit. Feel free to customize for your needs!

## License

MIT License - Free to use and modify

## Additional Resources

- [Official Selenium Documentation](https://www.selenium.dev/documentation/)
- [Selenium Python Bindings](https://selenium-python.readthedocs.io/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

---

**Built with best practices for browser automation in 2025**
