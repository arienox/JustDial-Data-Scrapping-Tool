# JustDial Data Scraper

An advanced web scraping solution designed to extract business information from JustDial. Built with Selenium and sophisticated anti-detection mechanisms for reliable data collection.

## Key Features

- **Comprehensive Data Collection:** Captures business details including names, locations, contact information, ratings, reviews, and website links
- **Intelligent Duplicate Management:** Built-in system to identify and eliminate duplicate entries
- **Advanced Anti-Blocking:** Implements multiple stealth techniques to prevent detection
- **Natural Interaction:** Simulates human behavior through randomized actions and movements
- **Enhanced Contact Detection:** Sophisticated algorithms for accurate phone number extraction
- **Versatile Input Options:** Supports both direct URLs and city/keyword search combinations
- **Structured Output:** Organizes collected data into well-formatted CSV files

## Prerequisites

- Python 3.x
- Google Chrome
- Python dependencies (install via `pip install -r requirements.txt`):
  - selenium
  - pandas
  - webdriver_manager

## Setup Instructions

1. Download the repository:
   ```bash
   git clone https://github.com/arienox/Just-Dial-Scrapper-Tool.git
   cd Just-Dial-Scrapper-Tool
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. Launch the program:
   ```bash
   python main.py
   ```

2. Select your preferred input method:
   - Direct URL input
   - City and keyword combination

3. The program will:
   - Import existing data to maintain uniqueness
   - Launch Chrome and access JustDial
   - Collect data while simulating natural browsing
   - Export results to a timestamped CSV file

## Detailed Features

### Duplicate Management System
- Cross-references with existing data files
- Prevents duplicate entries during active sessions
- Uses composite keys (name, address, phone) for uniqueness

### Anti-Detection System
- Variable timing between actions
- Natural scrolling behavior
- Randomized cursor movements
- Enhanced browser stealth settings
- Multiple content loading strategies

### Data Collection Capabilities
- Business Names
- Physical Addresses
- Contact Numbers (using multiple extraction techniques)
- Customer Ratings
- Review Counts
- Business Website Links

## Contributing

We welcome:
- Bug reports
- Feature suggestions
- Code contributions

## Legal Notice

This tool is intended for educational purposes. Users should review and adhere to JustDial's terms of service and robots.txt guidelines.

## Screenshots 

   ![image](https://github.com/user-attachments/assets/db720fd4-a662-4571-bcca-44fe20f242aa)
   ![image](https://github.com/user-attachments/assets/02af2345-6095-4a33-a229-ead54046abd5)

