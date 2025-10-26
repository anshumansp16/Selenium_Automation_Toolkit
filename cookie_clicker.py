import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(service=Service(executable_path="./chromedriver"))
driver.implicitly_wait(20)

driver.get("https://orteil.dashnet.org/cookieclicker/")







WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "langSelect-EN"))
)

#Step 1: Click on language button () ----> id = langSelect-EN
language_button = driver.find_element(By.ID, "langSelect-EN")
language_button.click()




# WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Got it!"))
# )

# #Step 2: Accept Cookies ----> Class = "cc_btn cc_btn_accept_all"
# accept_cookies = driver.find_element(By.PARTIAL_LINK_TEXT, "Got it!")
# accept_cookies.click()


WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)
#Step 3: Click on cookie button ----> id = bigCookie
cookie_button = driver.find_element(By.ID, "bigCookie")
cookies = driver.find_element(By.ID, "cookies")

counter = 1.6

while True:
    cookie_button.click()
    
    try:
          cookie_text = cookies.text.split()[0].replace(",", "")
          no_of_cookies = int(cookie_text)
    except (ValueError, IndexError) as e:
        print(f"Failed to parse cookies: {cookies.text}")
        continue

    print(f"No of cookies: {no_of_cookies}")

    if counter*10 < no_of_cookies:
        buy_buttons = driver.find_elements(By.CLASS_NAME, "enabled")

        # Find button with highest price
        max_price = 0
        most_expensive = None

        for button in buy_buttons:
            text_parts = button.text.split("\n")
            price_text = text_parts[-1].replace(",", "")

            # Check if price_text is valid before converting
            if price_text.isdigit():  # or use: if price_text.isdigit()
                price = int(price_text)
                if price > max_price:
                    max_price = price
                    most_expensive = button
        
        most_expensive.click()
        counter = counter*10
        print(f"I clicked and Counter updated to: {counter}")

time.sleep(1000)
driver.quit()



# 1. Literal Error
# 2. getting Max of Enabled Buy Buttons 
# 3. Clicking on most expensive button 