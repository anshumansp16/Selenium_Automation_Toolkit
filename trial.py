import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

driver.get('https://selenium.dev/documentation')
assert 'Selenium' in driver.title

time.sleep(10)
elem = driver.find_element(By.ID, 'm-documentationwebdriver')
elem.click()
assert 'WebDriver' in driver.title

def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    return options

options = get_default_chrome_options()
options.add_experimental_option("detach", True)
time.sleep(10)




driver.quit()