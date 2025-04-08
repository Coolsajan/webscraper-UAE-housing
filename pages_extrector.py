import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create folder if it doesn't exist
os.makedirs("Data", exist_ok=True)


page_no=1
# Setup WebDriver
while True :
    driver = webdriver.Chrome()
    driver.get(f"https://dubai.dubizzle.com/en/property-for-sale/residential/?page={page_no}")
    driver.maximize_window()
    
    # Wait for property cards to appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'property-lpv-card')]"))
    )
    
    # Get all card links first
    cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'property-lpv-card')]")
    print(f"Found {len(cards)} property cards.")
    
    links = []
    for card in cards:
        try:
            title_element = card.find_element(By.TAG_NAME, "a")
            link = title_element.get_attribute("href")
            if link:
                links.append(link)
        except:
            pass
    
    # Now visit each link and save the page
    for idx, link in enumerate(links):
        try:
            driver.get(link)
            time.sleep(3)  # Let page load, adjust if needed
    
            page_code = driver.page_source
    
            with open(f"Data/page_{page_no}_listing_{idx}.html", "w", encoding="utf-8") as f:
                f.write(page_code)
            print(f"Saved: page_{page_no}_listing_{idx}.html")
    
        except Exception as e:
            print(f"Error visiting {link}: {e}")
            continue
    driver.quit()    
    page_no +=1

driver.quit()
