"""
    Script for scraping laptops from newegg.

    Scrapes laptops from newegg and export it JSON.
    Raw data is exported to JSON.
"""
import json
from random import randint
from time import sleep
from typing import Generator, Tuple, Dict

import requests
from bs4 import BeautifulSoup, SoupStrainer, element

LAPTOP_URLS = [
    "https://www.newegg.com/Gaming-Laptops/SubCategory/ID-3365",
    # "https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32",
    # "https://www.newegg.com/Business-Laptops/SubCategory/ID-3413",
    # "https://www.newegg.com/Chromebooks/SubCategory/ID-3220"

]
MAXIUMUM_PAGES = 15
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
    "Safari/537.36"
)


def page_urls() -> Generator[str, None, None]:
    for url in LAPTOP_URLS:
        for page in range(1, MAXIUMUM_PAGES + 1):
            yield f"{url}/Page-{page}"


def laptop_urls() -> Generator[str, None, None]:
    for url in page_urls():
        soup = BeautifulSoup(get_html(url), features="lxml")
        random_sleep(10)
        items = soup.find_all(name="div", attrs={"class": "item-container"})

        for item in items:
            yield item.find("a").get("href")


def table_scraper(table: element.Tag) -> Tuple[str, Dict[str, str]]:
    name = table.find("caption").text
    rows = {
        row.find("th").text: row.find("td").text for row in table.find_all("tr")
    }
    return name, rows


def get_laptop_specs(html: str) -> Dict[str, Dict[str, str]]:
    specs = {}
    soup = BeautifulSoup(
        html,
        features="lxml",
        parse_only=SoupStrainer(name="div", attrs={"class": "tab-panes"}),
    )
    tables = soup.find_all("table")
    for table in tables:
        try:
            name, rows = table_scraper(table)
        except Exception as e:
            print(e)
        else:
            specs[name] = rows
    return specs


def get_html(url) -> str:
    html = requests.get(url, headers={"User-Agent": USER_AGENT}).text
    with open('test.html', 'w') as f:
        f.write(html)
    return html


def random_sleep(max_time: int) -> None:
    sleep(randint(1, max_time + 1))


def main() -> None:
    urls = list(laptop_urls())
    print(len(urls))
    # laptop_data = []
    # for index, laptop_url in enumerate(laptop_urls(), start=1):
    #     print(f"{laptop_url}- completed={index}")
    #     if index % 10 == 0:
    #         random_sleep(10)
    #     laptop_data.append(get_laptop_specs(get_html(laptop_url)))
    #
    # with open("raw_data.json", "w") as f:
    #     json.dump(laptop_data, f)


if __name__ == "__main__":
    main()
