# main.py

import time
import os
import csv
import threading
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils import check_and_click_close_popup, countdown_timer, smooth_scroll_to, human_like_scroll
import re

def get_url_input():
    # Ask the user if they have a URL or need to enter city/keyword
    print("Select an option:")
    print("1. Provide a URL")
    print("2. Enter City/Keyword")
    choice = input("Enter the number of your choice (1 or 2): ").strip()

    if choice == '1':
        url = input("Enter the URL: ").strip()
    elif choice == '2':
        city = input("Enter the city name: ").replace(' ', '-')
        keyword = input("Enter the search keyword: ").replace(' ', '-')
        base_url = "https://www.justdial.com/"
        url = f"{base_url}{city}/{keyword}/"
    else:
        print("Invalid choice. Exiting.")
        exit()

    return url

def get_url_from_file(filename):
    # Read the URL from the specified file
    try:
        with open(filename, 'r') as file:
            url = file.readline().strip()
            if url:
                return url
            else:
                print(f"The file '{filename}' is empty. Exiting.")
                exit()
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist. Exiting.")
        exit()

def load_existing_data():
    """
    Load existing data from all CSV files in the current directory.
    Returns a set of tuples (name, address, phone) representing existing entries.
    """
    existing_data = set()
    
    # Find all CSV files in the current directory
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and not f.endswith('_filtered.csv')]
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            # Create a set of tuples (name, address, phone) for each row
            for _, row in df.iterrows():
                # Handle missing values
                name = str(row.get('Name', '')).strip()
                address = str(row.get('Address', '')).strip()
                phone = str(row.get('Phone', '')).strip()
                
                if name and (address or phone):  # Only add if we have at least name and one other field
                    existing_data.add((name, address, phone))
            
            print(f"Loaded {len(existing_data)} existing entries from {csv_file}")
        except Exception as e:
            print(f"Error loading {csv_file}: {str(e)}")
    
    return existing_data

def is_duplicate(name, address, phone, existing_data):
    """
    Check if a result is a duplicate of existing data.
    """
    name = str(name).strip()
    address = str(address).strip()
    phone = str(phone).strip()
    
    return (name, address, phone) in existing_data

def extract_data(driver, writer, existing_data):
    # Wait for the results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'resultbox_info'))
    )
    
    # Find all store details
    store_details = driver.find_elements(By.CLASS_NAME, 'resultbox_info')
    results_count = 0
    new_results_count = 0
    
    for store in store_details:
        try:
            # Extract name and webpage URL
            name_element = store.find_element(By.CLASS_NAME, 'resultbox_title_anchor')
            name = name_element.text.strip()
            
            # Get the webpage URL using multiple methods
            webpage_url = None
            try:
                # Method 1: Direct href attribute
                webpage_url = name_element.get_attribute('href')
                
                # Method 2: onclick attribute
                if not webpage_url:
                    onclick = name_element.get_attribute('onclick')
                    if onclick:
                        if 'window.location.href' in onclick:
                            webpage_url = onclick.split('window.location.href=')[1].strip("'")
                        elif 'window.location=' in onclick:
                            webpage_url = onclick.split('window.location=')[1].strip("'")
                
                # Method 3: data-url attribute
                if not webpage_url:
                    webpage_url = name_element.get_attribute('data-url')
                
                # Method 4: Try to find URL in parent element
                if not webpage_url:
                    parent = name_element.find_element(By.XPATH, '..')
                    webpage_url = parent.get_attribute('href')
                
                # Method 5: Try to find URL in any child elements
                if not webpage_url:
                    try:
                        url_element = name_element.find_element(By.CSS_SELECTOR, '[href*="justdial.com"]')
                        webpage_url = url_element.get_attribute('href')
                    except:
                        pass
                
                # Clean up the URL if found
                if webpage_url:
                    webpage_url = webpage_url.strip()
                    if not webpage_url.startswith('http'):
                        webpage_url = 'https://www.justdial.com' + webpage_url
            except Exception as e:
                print(f"Error extracting URL for {name}: {str(e)}")
                pass
            
            # Extract address
            address_element = store.find_element(By.CLASS_NAME, 'resultbox_address')
            address = address_element.text.strip()
            
            # Extract phone - using multiple methods
            phone = "N/A"
            try:
                # Method 1: Try the original class
                try:
                    phone_element = store.find_element(By.CLASS_NAME, 'callcontent')
                    phone = phone_element.text.strip()
                except:
                    pass
                
                # Method 2: Try alternative class names
                if phone == "N/A":
                    for class_name in ['callcontent', 'phone', 'contact', 'mobile', 'telephone']:
                        try:
                            phone_element = store.find_element(By.CLASS_NAME, class_name)
                            phone = phone_element.text.strip()
                            if phone:
                                break
                        except:
                            continue
                
                # Method 3: Try CSS selectors
                if phone == "N/A":
                    for selector in ['[class*="phone"]', '[class*="call"]', '[class*="contact"]', '[class*="mobile"]']:
                        try:
                            phone_element = store.find_element(By.CSS_SELECTOR, selector)
                            phone = phone_element.text.strip()
                            if phone:
                                break
                        except:
                            continue
                
                # Method 4: Look for phone numbers in the entire store element
                if phone == "N/A":
                    store_text = store.text
                    # Look for patterns like +91-XXXXXXXXXX or XXXXXXXXXX
                    phone_matches = re.findall(r'(\+91[\s-]?\d{10}|\d{10})', store_text)
                    if phone_matches:
                        phone = phone_matches[0]
                
                # Clean up the phone number
                if phone != "N/A":
                    # Remove any non-digit characters except + and -
                    phone = re.sub(r'[^\d+\-]', '', phone)
            except Exception as e:
                print(f"Error extracting phone for {name}: {str(e)}")
                phone = "N/A"
            
            # Extract rating - using the new selector
            try:
                rating_element = store.find_element(By.CSS_SELECTOR, 'div[class*="resultbox_totalrate"]')
                rating = rating_element.text.split()[0]  # Get just the number, not the star
            except:
                rating = "N/A"
                
            # Extract number of ratings - using the new selector
            try:
                reviews_element = store.find_element(By.CSS_SELECTOR, 'div[class*="resultbox_countrate"]')
                reviews = reviews_element.text.strip()  # This will get "X Ratings"
            except:
                reviews = "N/A"
            
            if name and (address or phone):  # Allow missing address or phone
                # Check if this is a duplicate
                if not is_duplicate(name, address, phone, existing_data):
                    writer.writerow({
                        'Name': name,
                        'Address': address,
                        'Phone': phone,
                        'Rating': rating,
                        'Reviews': reviews,
                        'Webpage': webpage_url
                    })
                    new_results_count += 1
                    # Add to existing data to prevent duplicates within the same session
                    existing_data.add((name, address, phone))
                    print(f"Found new result: {name} (Rating: {rating}, Reviews: {reviews}, Webpage: {webpage_url})")
                else:
                    print(f"Skipping duplicate: {name}")
                
                results_count += 1
                
        except Exception as e:
            continue  # Skip this entry if there's an error
            
    return results_count, new_results_count

# Get the URL from temp_url.txt if it exists
if os.path.exists('temp_url.txt'):
    url = get_url_from_file('temp_url.txt')
else:
    # Use the original URL fetching method if temp_url.txt does not exist
    url = get_url_input()

# Load existing data to avoid duplicates
print("Loading existing data to avoid duplicates...")
existing_data = load_existing_data()
print(f"Loaded {len(existing_data)} existing entries to check against")

# Set up Chrome options with additional stealth
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-popup-blocking")

# Additional stealth settings
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "webrtc.ip_handling_policy": "disable_non_proxied_udp"
}
chrome_options.add_experimental_option("prefs", prefs)

# Set up WebDriver with stealth
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Additional stealth
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """
})

# Start the countdown timer in a separate thread (increased to 300 seconds)
countdown_thread = threading.Thread(target=countdown_timer, args=(300,))
countdown_thread.start()

try:
    # Add random initial delay
    time.sleep(random.uniform(2, 5))
    
    driver.get(url)
    print("Opened URL:", url)

    # Random delay after page load
    time.sleep(random.uniform(8, 12))

    # Handle popups with retry
    for _ in range(3):  # Try 3 times
        try:
            # Look for various popup close buttons
            popup_selectors = [
                (By.CLASS_NAME, 'maybelater'),
                (By.CLASS_NAME, 'close'),
                (By.CLASS_NAME, 'popup-close'),
                (By.XPATH, "//button[contains(text(), 'Later')]"),
                (By.XPATH, "//button[contains(text(), 'Close')]")
            ]
            
            for selector_type, selector in popup_selectors:
                try:
                    popup = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((selector_type, selector))
                    )
                    if popup.is_displayed():
                        popup.click()
                        print(f"Clicked popup with selector: {selector}")
                        time.sleep(random.uniform(1, 2))
                except:
                    continue
            
            break  # If we get here without exception, break the retry loop
        except Exception as e:
            print(f"Attempt to handle popup failed: {str(e)}")
            time.sleep(2)

    # Generate filename with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    csv_filename = f"results_{url.split('/')[-2]}_{timestamp}.csv"
    csv_filepath = os.path.join(os.getcwd(), csv_filename)

    print(f"\nWill save results to: {csv_filepath}")

    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Rating', 'Reviews', 'Webpage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Start scrolling and collecting data
        total_results = 0
        total_new_results = 0
        last_results_count = 0
        no_new_results_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 10  # Decreased from 50 to 10
        
        # Continue scrolling until we have enough results or reach max attempts
        while (no_new_results_count < 8 and scroll_attempts < max_scroll_attempts) or total_new_results < 50:
            scroll_attempts += 1
            print(f"\nScroll attempt {scroll_attempts}/{max_scroll_attempts}")
            
            # Random mouse movements
            if random.random() < 0.3:  # 30% chance
                try:
                    elements = driver.find_elements(By.TAG_NAME, "div")
                    if elements:
                        random_element = random.choice(elements)
                        action = webdriver.ActionChains(driver)
                        action.move_to_element(random_element).perform()
                except:
                    pass
            
            # Enhanced scrolling behavior
            if scroll_attempts % 3 == 0:
                print("\nUsing alternative scroll pattern...")
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                random_position = random.randint(scroll_height // 4, scroll_height * 3 // 4)
                smooth_scroll_to(driver, random_position, duration=random.uniform(1.5, 2.5))
            else:
                # More aggressive scrolling to load more content
                human_like_scroll(driver, scroll_amount=random.randint(800, 1200))
            
            # Random wait between scrolls
            time.sleep(random.uniform(2, 4))
            
            # Extract data
            new_results, new_unique_results = extract_data(driver, writer, existing_data)
            total_new_results += new_unique_results
            
            if new_results > last_results_count:
                print(f"\nFound {new_results - last_results_count} results, {new_unique_results} new unique results. Total: {new_results}, New unique: {total_new_results}")
                last_results_count = new_results
                no_new_results_count = 0
            else:
                no_new_results_count += 1
                print(f"\nNo new results found. Attempt {no_new_results_count}/8")
            
            total_results = new_results
            
            # Try different strategies when stuck
            if no_new_results_count >= 3:
                print("\nTrying alternative loading strategies...")
                
                # Strategy 1: Click "Show More" buttons
                try:
                    show_more_buttons = driver.find_elements(By.CSS_SELECTOR, 
                        '[class*="show_more"], [class*="load_more"], [class*="showMore"], button:contains("more")')
                    for button in show_more_buttons:
                        if button.is_displayed():
                            button.click()
                            print("Clicked 'Show More' button")
                            time.sleep(random.uniform(3, 5))
                            no_new_results_count = 0
                            break
                except:
                    pass
                
                # Strategy 2: Try refreshing the page
                if random.random() < 0.3:  # 30% chance
                    print("\nRefreshing page...")
                    driver.refresh()
                    time.sleep(random.uniform(8, 10))
                    no_new_results_count = 0
                
                # Strategy 3: Try different viewport positions
                if random.random() < 0.5:  # 50% chance
                    window_height = driver.execute_script("return window.innerHeight")
                    scroll_height = driver.execute_script("return document.body.scrollHeight")
                    positions = [
                        scroll_height // 4,
                        scroll_height // 2,
                        (scroll_height * 3) // 4
                    ]
                    random.shuffle(positions)
                    for pos in positions:
                        smooth_scroll_to(driver, pos, duration=random.uniform(1, 2))
                        time.sleep(random.uniform(2, 3))
                
                # Strategy 4: Try clicking on pagination links if available
                if random.random() < 0.4:  # 40% chance
                    try:
                        pagination_links = driver.find_elements(By.CSS_SELECTOR, 
                            '[class*="pagination"] a, [class*="page-link"], a[href*="page="]')
                        if pagination_links:
                            random_link = random.choice(pagination_links)
                            if random_link.is_displayed():
                                random_link.click()
                                print("Clicked pagination link")
                                time.sleep(random.uniform(5, 7))
                                no_new_results_count = 0
                    except:
                        pass

    print(f"\nData extraction completed. Total results: {total_results}, New unique results: {total_new_results}")
    print(f"Data saved to '{csv_filepath}'.")

except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")

finally:
    # Clean up
    if os.path.exists('page_source.html'):
        os.remove('page_source.html')
    if os.path.exists('stop.txt'):
        os.remove('stop.txt')
    if os.path.exists('error_log.txt'):
        os.remove('error_log.txt')
    print("Cleanup completed.")
    
    # Close the browser
    driver.quit()

