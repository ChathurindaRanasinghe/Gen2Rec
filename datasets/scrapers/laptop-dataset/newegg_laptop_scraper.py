"""
    Script for scraping laptops from newegg.
    Scrapes laptops from newegg and export raw data to JSON.

    Usage:
        python dataset/laptop-dataset/newegg_laptop_scraper.py -mp 1

        mp: Number of pages to scrape for each category
            One page contain approximately have 40 laptops
"""

import json
import os
from argparse import ArgumentParser
from datetime import datetime
from random import randint
from time import sleep
from typing import Generator, Tuple, Dict, Any

import requests
from bs4 import BeautifulSoup, SoupStrainer, element

CATEGORIES = [
    "https://www.newegg.com/Gaming-Laptops/SubCategory/ID-3365",  # gaming laptops
    "https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32",  # notebooks
    "https://www.newegg.com/Business-Laptops/SubCategory/ID-3413",  # business laptops
    "https://www.newegg.com/Chromebooks/SubCategory/ID-3220",  # chromebooks
]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
    "Safari/537.36"
)


def page_urls(max_pages: int) -> Generator[str, None, None]:
    for url in CATEGORIES:
        for page in range(1, max_pages + 1):
            yield f"{url}/Page-{page}"


def laptop_urls(max_pages: int) -> Generator[str, None, None]:
    return (
        item.find("a").get("href")
        for url in page_urls(max_pages)
        for item in
        BeautifulSoup(get_html(url), features="lxml").find_all(name="div", attrs={"class": "item-container"})
    )


def table_scraper(table: element.Tag) -> Tuple[str, Dict[str, str]] | Tuple[None, None]:
    try:
        name = table.find("caption").text
        rows = {row.find("th").text: row.find("td").text for row in table.find_all("tr")}
        return name, rows
    except AttributeError:
        return None, None


def get_laptop_specs(html: str) -> Dict[str, Dict[str, str]]:
    soup = BeautifulSoup(
        html,
        features="lxml",
        parse_only=SoupStrainer(name="div", attrs={"class": "tab-panes"}),
    )
    return dict(filter(lambda x: x[0] is not None, map(table_scraper, soup.find_all("table"))))


def get_html(url: str) -> str:
    return requests.get(url, headers={"User-Agent": USER_AGENT}).text


def random_sleep(max_time: int) -> None:
    sleep_time = randint(1, max_time + 1)
    print(f"Sleeping for {sleep_time} seconds ...")
    sleep(sleep_time)


def get_file_name(max_pages: int) -> str:
    datetime_format = "%d_%b_%Y_%H_%M_%S.%f"
    return os.path.join("datasets", "laptop-dataset", "data",
                        f"raw_data_mp{max_pages}_{datetime.now().strftime(datetime_format)}.json")


def process_laptop(index: int, url: str) -> Dict[Any, Any]:
    print(f"{url} - completed={index}")
    if index % 10 == 0:
        random_sleep(10)
    return get_laptop_specs(get_html(url))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("-mp", "--max-pages", type=int)
    args = parser.parse_args()

    laptop_data = list(map(lambda x: process_laptop(x[0], x[1]), enumerate(laptop_urls(args.max_pages), start=1)))

    with open(get_file_name(args.max_pages), "w") as f:
        json.dump(laptop_data, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
