import time
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

print("Opening Google")
driver.get("https://www.google.com")

print("Waiting for search box")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)

print("Searching for Anshuman Parmar")
search = driver.find_element(By.CLASS_NAME, "gLFyf")
search.send_keys("Ansh c casdlck")

print("Waiting for search box to be cleared")
time.sleep(5)

print("Clearing search box")
search.clear()

print("Sending keys to search box")
search.send_keys("Anshuman Parmar" + Keys.ENTER)


print("Waiting for link to be found")
WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Anshuman Parmar - Entrepreneur"))
)


elements = driver.find_elements(By.TAG_NAME, 'h3')


print("Printing elements")
for e in elements:
    print(e.text)
    time.sleep(5)



print("Finding link")
link = driver.find_element(By.PARTIAL_LINK_TEXT, "Anshuman Parmar - Entrepreneur")

print("Clicking link")
link.click()

driver.switch_to.new_window('tab')

print("Waiting for 10 seconds")
time.sleep(10)



print("Quitting driver")
driver.quit()