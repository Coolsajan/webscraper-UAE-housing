import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

import time
import random
import traceback

# Create folder if it doesn't exist
os.makedirs("Data", exist_ok=True)



# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    with webdriver.Chrome(options=options) as driver:
        visited_links = set()
        for i in range(18, 2287):  # Test with a small range first
            url = f"https://dubai.dubizzle.com/en/property-for-sale/residential/?page={i}"
            print(f"Scraping page {i}...")
            driver.get(url)
            driver.minimize_window()

            # Wait for property cards to load with extended timeout
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'property-lpv-card')]"))
                )
                print(f"Page {i} loaded successfully.")
            except TimeoutException as e:
                print(f"Timeout waiting for elements on page {i}: {e}")
                print("Page source for debugging:")
                print(driver.page_source[:1000])  # Print first 1000 chars of page source
                continue
            except Exception as e:
                print(f"Unexpected error loading page {i}: {traceback.format_exc()}")
                continue

            # Get all card links
            cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'property-lpv-card')]")
            print(f"Found {len(cards)} property cards on page {i}.")

            links = []
            for card in cards:
                try:
                    title_element = card.find_element(By.TAG_NAME, "a")
                    link = title_element.get_attribute("href")
                    if link and link not in visited_links:
                        links.append(link)
                        visited_links.add(link)
                except Exception as e:
                    print(f"Error extracting link: {traceback.format_exc()}")

            # Visit each link and save the page
            for idx, link in enumerate(links):
                try:
                    driver.get(link)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//h1"))  # Adjust XPath for detail page
                    )

                    page_code = driver.page_source
                    filename = f"Data/page_{i}_listing_{idx}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(page_code)
                    print(f"Saved: {filename}")

                    time.sleep(random.uniform(1, 3))

                except Exception as e:
                    print(f"Error visiting {link}: {traceback.format_exc()}")

except WebDriverException as e:
    print(f"WebDriver setup failed: {traceback.format_exc()}")

print("Scraping completed!")