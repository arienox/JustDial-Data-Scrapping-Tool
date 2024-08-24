# JustDial Data Scraping Script

This script uses Selenium to scrape data from Justdial. It automates the process of opening a webpage, handling popups, scrolling, and extracting contact information, then saves the data into a CSV file.

It currently scrapes Name, Address, and Phone numbers from a given city and keyword.

## Features

- **Dynamic URL Generation:** Constructs the URL based on user input for city and keyword.
- **Popup Handling:** Automatically closes certain popups that may interfere with scraping.
- **Human-like Scrolling:** Scrolls the page smoothly to load more content.
- **Data Extraction:** Collects names, addresses, and phone numbers.
- **Data Saving:** Saves the extracted data in a CSV file within a `Scrapped` folder, named after the search keyword.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone or Download the Repository**

   Clone the repository to your local machine or download the script file:

   ```sh
   git clone https://github.com/r7avi/JustDial-Data-Scrapper.git
   cd JustDial-Data-Scrapper
   pip install -r requirements.txt

## Screenshots 

   ![image](https://github.com/user-attachments/assets/db720fd4-a662-4571-bcca-44fe20f242aa)

