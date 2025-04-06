# Just-Dial-Scrapper-Tool

A powerful web scraping tool for extracting business information from JustDial. This tool uses Selenium with advanced anti-detection measures to reliably scrape business listings.

## Features

- **Smart Data Extraction:** Extracts business names, addresses, phone numbers, ratings, reviews, and webpage URLs
- **Duplicate Prevention:** Automatically checks for and filters out duplicate entries
- **Anti-Detection Measures:** Uses various stealth techniques to avoid being blocked
- **Human-like Behavior:** Implements random delays, scrolling patterns, and mouse movements
- **Robust Phone Number Extraction:** Multiple methods to reliably extract contact information
- **Flexible Input:** Accept direct URLs or city/keyword combinations
- **CSV Export:** Saves data in a clean, organized CSV format

## Requirements

- Python 3.x
- Chrome Browser
- Required Python packages (install using `pip install -r requirements.txt`):
  - selenium
  - pandas
  - webdriver_manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arienox/Just-Dial-Scrapper-Tool.git
   cd Just-Dial-Scrapper-Tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Choose your input method:
   - Option 1: Provide a direct JustDial URL
   - Option 2: Enter city name and search keyword

3. The script will:
   - Load any existing data to prevent duplicates
   - Open Chrome and navigate to JustDial
   - Start collecting data while scrolling
   - Save results to a timestamped CSV file

## Features in Detail

### Duplicate Prevention
- Checks against existing CSV files
- Prevents duplicate entries within the same session
- Uses business name, address, and phone as unique identifiers

### Anti-Detection Measures
- Random delays between actions
- Human-like scrolling patterns
- Random mouse movements
- Stealth mode configurations
- Multiple strategies for loading more content

### Data Extraction
- Business Names
- Addresses
- Phone Numbers (multiple extraction methods)
- Ratings
- Number of Reviews
- Webpage URLs

## Contributing

Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

## Disclaimer

This tool is for educational purposes only. Please check and comply with JustDial's terms of service and robots.txt before using this tool.

## Screenshots 

   ![image](https://github.com/user-attachments/assets/db720fd4-a662-4571-bcca-44fe20f242aa)
   ![image](https://github.com/user-attachments/assets/02af2345-6095-4a33-a229-ead54046abd5)

