import time
import random
import threading
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Ask for city and keyword inputs
city = input("Enter the city name: ").replace(' ', '-')
keyword = input("Enter the search keyword: ").replace(' ', '-')

# Generate URL based on inputs
base_url = "https://www.justdial.com/"
url = f"{base_url}{city}/{keyword}/"

# Set up Chrome options
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Hide WebDriver signature
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def check_and_click_close_popup(driver):
    """Check for the close popup button and click it if found."""
    try:
        close_popup_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'jd_modal_close'))
        )
        if close_popup_button.is_displayed():
            close_popup_button.click()
            print("Clicked 'jd_modal_close' button.")
            return True
    except:
        pass  # Silence the exception and avoid printing the error message
    return False

def countdown_timer(seconds):
    """Display a countdown timer in the console."""
    for i in range(seconds, 0, -1):
        print(f"Time remaining: {i} seconds", end='\r')
        time.sleep(1)
    print("Time's up! Stop file will be created.")
    with open('stop.txt', 'w') as f:
        f.write('')

# Start the countdown timer in a separate thread
countdown_thread = threading.Thread(target=countdown_timer, args=(20,))
countdown_thread.start()

try:
    driver.get(url)
    print("Opened URL:", url)

    # Check for 'Maybe Later' popup and click it if found
    time.sleep(5)
    try:
        maybe_later_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'maybelater'))
        )
        if maybe_later_button.is_displayed():
            maybe_later_button.click()
            print("Clicked 'Maybe Later' button.")
    except Exception as e:
        print(f"Maybe Later popup not found or failed to click: {str(e)}")

    # Function to perform smooth, human-like scrolling
    def human_like_scroll(driver, max_scroll_attempts=5, scroll_pause_range=(1, 3), stop_file='stop.txt'):
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        
        while scroll_attempts < max_scroll_attempts:
            # Check if stop file exists
            if os.path.exists(stop_file):
                print("Stop file detected. Stopping scroll.")
                break
            
            driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
            
            # Check and handle the popup button
            check_and_click_close_popup(driver)
            
            time.sleep(random.uniform(*scroll_pause_range))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0  # Reset if new content is loaded
            last_height = new_height

        print("Scrolling completed.")

    human_like_scroll(driver)

    # Fetch and save page source for debugging
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("Page source saved to 'page_source.html'.")

    # Ensure the 'Scrapped' folder exists
    os.makedirs('Scrapped', exist_ok=True)

    # Find and save data in CSV
    csv_filename = os.path.join('Scrapped', f"{keyword}.csv")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        parent_divs = driver.find_elements(By.CLASS_NAME, 'resultbox_info')
        if not parent_divs:
            print("No parent divs found. Check the class name and page source.")
        else:
            for index, parent_div in enumerate(parent_divs):
                try:
                    name_div = parent_div.find_element(By.CLASS_NAME, 'resultbox_title_anchor')
                    name = name_div.text.strip()
                    phone_div = parent_div.find_element(By.CLASS_NAME, 'callcontent')
                    phone_number = phone_div.text.strip()
                    address_div = parent_div.find_element(By.CLASS_NAME, 'resultbox_address')  # Updated to include address
                    address = address_div.text.strip()

                    if name and phone_number and address:
                        writer.writerow({'Name': name, 'Address': address, 'Phone': phone_number})
                    else:
                        print(f"Missing data in parent div {index}. Name: '{name}', Address: '{address}', Phone: '{phone_number}'")

                except Exception as e:
                    with open('error_log.txt', 'a', encoding='utf-8') as error_file:
                        error_file.write(f"An error occurred in parent div {index}: {str(e)}\n")

    print(f"Data extraction completed and saved to '{csv_filename}'.")

except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")

finally:
    # Print script completion message
    print("Script execution completed. Browser will remain open.")
    
    # Wait for 3 seconds
    time.sleep(3)
    
    # Remove page_source.html and stop.txt files
    if os.path.exists('page_source.html'):
        os.remove('page_source.html')
    if os.path.exists('stop.txt'):
        os.remove('stop.txt')
    
    # Keep the browser open, looping indefinitely until manually closed
    while True:
        time.sleep(10)
