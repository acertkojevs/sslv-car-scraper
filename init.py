"""Import dependencies"""
import re
import warnings
import requests
from bs4 import BeautifulSoup
import pandas as pd
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)




class WebScrapper:
    """A web scraper class to fetch and parse HTML content from multiple pages."""

    def __init__(self):
        self.base_url = None
        self._response = None
        self._soup = None
        self._data = []
        self.__visited_urls = set()

    def _fetch_page(self, url, timeout=10):
        """fetch page with a timeout to prevent hanging indefinitely."""
        try:
            self._response  = requests.get(url, timeout=timeout)
            self._response.raise_for_status()
            if self._response.url == "https://www.ss.lv/lv/":
                print(f"Invalid car type URL, redirected to home page: {url}")
                return False
            self._soup = BeautifulSoup(self._response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print("Error fetching page:", e)

    def _scrape_multiple_pages(self):
        """iterator trought each page"""
        counter = 1
        while True:
            url = self.base_url if counter == 1 else f"{self.base_url}page{counter}.html"
            self._fetch_page(url)
            if self._response:  # Check if there's a response object
                current_url = self._response.url  # Get the URL of the current response
                if current_url in self.__visited_urls:
                    print(f"Already visited page: {current_url}. Ending iterations.")
                    break
                self.__visited_urls.add(current_url)

            if not self._soup:
                print("Page not fetched. Call fetch_page() first.")
                return

            if not self._soup.find("table",align="center",cellpadding="2",cellspacing="0",border="0",width="100%"):
                return

            data = self._scrape_table()
            if data is not None:
                self._data.append(data)
                print(self._data)
                counter += 1
            else:
                break

        self.__export_to_csv()
    def _scrape_table(self):
        """Scrape page table"""
        if not self._soup:
            print("Page not fetched. Call fetch_page() first.")
            return

        table = self._soup.find(
            "table",
            align="center",
            cellpadding="2",
            cellspacing="0",
            border="0",
            width="100%"
        )

        data_set = {
            "desc": [],
            "link": [],
            "model": [],
            "year": [],
            "capacity": [],
            "mileage": [],
            "price": [],
        }

        if table:
            # Use find_all to find all <tr> tags within the table
            tr_tags = table.find_all("tr")  # type: ignore
            for tr_tag in tr_tags[1:-1]:  # Skip first and last tr tag
                # Find all <td> tags within the current <tr> tag
                td_tags = tr_tag.find_all("td")
                for index, td_tag in enumerate(td_tags[2:]):
                    match index:
                        case 0:
                            desc = td_tag.get_text(strip=True)
                            data_set["desc"].append(desc)

                            inner_tag = td_tag.find("a")
                            if inner_tag:
                                # Extract the text value of the inner tag
                                href_value = inner_tag.get("href")
                                link = f"www.ss.lv{href_value}"
                                data_set["link"].append(link)
                        case 1:
                            model = td_tag.get_text(strip=True)
                            data_set["model"].append(model)
                        case 2:
                            year = td_tag.get_text(strip=True)
                            data_set["year"].append(year)
                        case 3:
                            capacity = td_tag.get_text(strip=True)
                            data_set["capacity"].append(capacity)
                        case 4:
                            mileage = td_tag.get_text(strip=True)
                            data_set["mileage"].append(mileage)
                        case 5:
                            price = td_tag.get_text(strip=True)
                            data_set["price"].append(price)

            df = pd.DataFrame(data_set)
            return df
        else:
            print("No main table found with width 100%.")

    def __export_to_csv(self):
        """Export the collected data to a CSV file."""
        if self._data:
            df = pd.concat(self._data, ignore_index=True)
            df.to_csv("scraped_data.csv", index=False, encoding='utf-8-sig')
            print(f"Data exported to {"scraped_data.csv"}")
        else:
            print("No data to export.")

    def check_url(self):
        """URL validating."""
        input_url = input('SS.LV Car URL:')
        pattern = r"^https://www\.ss\.lv/lv/transport/cars/[^/]+/?$"
        result = re.match(pattern, input_url)

        self._fetch_page(input_url)

        if result and self._response:
            self.base_url = input_url
            self._scrape_multiple_pages()
        else:
            print("Invalid URL or car type.")
            return False
# URL = "https://www.ss.lv/lv/transport/cars/jaguar/"
scraper = WebScrapper()
URL = scraper.check_url()
