# utils.py

import time
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def smooth_scroll_to(driver, target_position, duration=2):
    """Smoothly scroll the page to a target position."""
    start_position = driver.execute_script("return window.pageYOffset")
    distance = target_position - start_position
    start_time = time.time()
    
    while time.time() - start_time < duration:
        elapsed_time = time.time() - start_time
        scroll_position = start_position + (distance * (elapsed_time / duration))
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(0.1)  # Adjust sleep time for smoother scrolling

    # Ensure we end exactly at the target position
    driver.execute_script(f"window.scrollTo(0, {target_position});")

def human_like_scroll(driver, min_scroll_down=15, max_scroll_down=20, min_scroll_up=12, max_scroll_up=15, scroll_pause_range=(0.5, 1.5), stop_file='stop.txt', scroll_amount=None):
    """
    Scroll the page in a human-like manner with random pauses and occasional scrolls up.
    
    Args:
        driver: The Selenium WebDriver instance
        min_scroll_down: Minimum pixels to scroll down
        max_scroll_down: Maximum pixels to scroll down
        min_scroll_up: Minimum pixels to scroll up
        max_scroll_up: Maximum pixels to scroll up
        scroll_pause_range: Range of seconds to pause between scrolls
        stop_file: File to check for stopping the scrolling
        scroll_amount: Optional specific amount to scroll (overrides min/max_scroll_down)
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_position = driver.execute_script("return window.pageYOffset")
    
    # Check if stop file exists
    if os.path.exists(stop_file):
        print(f"Stop file '{stop_file}' detected. Stopping scroll.")
        return
    
    # Determine scroll amount
    if scroll_amount is not None:
        pixels_to_scroll = scroll_amount
    else:
        pixels_to_scroll = random.randint(min_scroll_down, max_scroll_down)
    
    # Scroll down
    new_position = last_position + pixels_to_scroll
    driver.execute_script(f"window.scrollTo(0, {new_position});")
    
    # Random pause
    pause_time = random.uniform(scroll_pause_range[0], scroll_pause_range[1])
    time.sleep(pause_time)
    
    # Occasionally scroll up a bit (20% chance)
    if random.random() < 0.2:
        pixels_up = random.randint(min_scroll_up, max_scroll_up)
        up_position = max(0, new_position - pixels_up)
        driver.execute_script(f"window.scrollTo(0, {up_position});")
        time.sleep(random.uniform(scroll_pause_range[0], scroll_pause_range[1]))
        driver.execute_script(f"window.scrollTo(0, {new_position});")
    
    # Check if we've reached the bottom
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # Try to trigger loading more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 2))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 500);")
        time.sleep(random.uniform(1, 2))


