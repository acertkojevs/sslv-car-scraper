# SSLV Car Scraper

A web scraper for extracting car listings from ss.lv, a popular classifieds website. This tool fetches data such as descriptions, links, models, years, capacities, mileage, and prices from multiple pages and exports it to a CSV file for easy analysis and use.

## Features

- Fetches car listings from ss.lv
- Extracts detailed information including description, link, model, year, engine capacity, mileage, and price
- Handles multiple pages of listings
- Exports data to a CSV file

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/NutellaON/sslv-car-scraper.git
   cd sslv-car-scraper
2. Install required depencies
   ```bash
   pip install -r requirements.txt

4. Run the scraper:
   ```bash
   python scraper.py

## Usage
When you run the script, you will be prompted to enter a URL from the ss.lv car listings page.
The scraper will fetch data from multiple pages and save it to "scraped_data.csv".
Dependencies
requests: For making HTTP requests to fetch web pages.
beautifulsoup4: For parsing HTML and extracting data.
pandas: For data manipulation and exporting to CSV.
## Example
To use the scraper, provide the URL of the car listings page when prompted. For example:

SS.LV Car URL: https://www.ss.lv/lv/transport/cars/jaguar/
The scraper will then process the data and export it to a CSV file named "scraped_data.csv".
