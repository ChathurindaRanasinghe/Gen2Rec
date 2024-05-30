import json
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WEBSITE_URL = "https://www.usedcars.com"
# PARAMS = ["/buy"]
PARAMS = ["/buy/bodyTypes-convertible",
          "/buy/bodyTypes-coupe",
          "/buy/bodyTypes-hatchback",
          "/buy/bodyTypes-minivan",
          "/buy/bodyTypes-sedan",
          "/buy/bodyTypes-suv",
          "/buy/bodyTypes-truck",
          "/buy/bodyTypes-van",
          "/buy/bodyTypes-wagon"]
DRIVER_PATH = "D:/Inbox/project-Gen2Rec/chromedriver-win64/chromedriver.exe"


def get_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    return webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)


def get_content(driver: WebDriver, param: str, level: int) -> str:
    print(WEBSITE_URL + param)
    driver.get(WEBSITE_URL + param)
    sleep(10)
    for x in range(0, level):
        print("level " + str(x + 1))
        button = None
        not_found = 0
        page_end = False
        while not button:
            if not_found > 40:
                page_end = True
                break
            driver.execute_script("window.scrollBy(0, 500);")
            sleep(1)
            try:
                button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "sc-bb59fb03-5"))
                )
                print("Button found")
                break
            except:
                not_found += 1
                print("Button not found")
        if page_end:
            break
        try:
            button.click()
            print("Button clicked")
        except:
            driver.execute_script("window.scrollBy(0, -1000);")
        sleep(5)
    return driver.page_source


def scrape_links(content: str) -> list:
    soup = BeautifulSoup(content, "html.parser")
    vehicle_elements = soup.find_all("a", {"class": "sc-5a680332-4 jEbBWJ"})
    vehicle_links = [element["href"] for element in vehicle_elements]
    print("number 0f vehicles: " + str(len(vehicle_links)))
    return vehicle_links


def save_links(vehicle_links: list, filename: str) -> None:
    with open(filename, "a") as file:
        for link in vehicle_links:
            file.write(link + "\n")


def get_links(filename: str) -> None:
    driver = get_driver()
    for param in PARAMS:
        content = get_content(driver, param, level=80)
        vehicle_links = scrape_links(content)
        save_links(vehicle_links, filename)
    driver.quit()


def read_links(input_filename: str) -> list:
    vehicle_links = []
    with open(input_filename, "r") as file:
        for line in file:
            vehicle_links.append(line.strip())
    return vehicle_links


def scrape_details(soup: BeautifulSoup) -> dict:
    try:
        details = {
            "name": soup.find("h1", {"class": "sc-62e5a65e-0 kWFIdk"}).text.strip(),
            "price": soup.find("p", {"class": "sc-35cccf38-16 lijBWx"}).text.strip(),
            "overview": [span.text.strip() for span in soup.find_all("span", {"class": "sc-d13ff064-4 jXiDwC"})],
            "features": [span.text.strip() for span in soup.find_all("span", {"class": "sc-11aa6444-3 edIwFs"})],
            "history": [span.text.strip() for span in soup.find_all("div", {"class": "sc-8f7178d0-9 lfhAiN"})],
            "seller_notes": soup.find("span", {"id": "seller-notes-text"}).text.strip(),
            "seller": soup.find("h3", {"class": "sc-5880c977-3 egrhEm"}).text.strip()
        }
        if soup.find("div", {"class": "sc-f4e7e306-2 iFfVqN"}):
            details["review"] = soup.find("div", {"class": "sc-f4e7e306-2 iFfVqN"}).text.strip()
        return details
    except:
        print("error scraping details")


def get_details(input_filename: str, output_filename: str) -> None:
    links = read_links(input_filename)
    detail_list = []
    driver = get_driver()
    for link in links:
        try:
            driver.get(WEBSITE_URL + link)
            sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            details = scrape_details(soup)
            detail_list.append(details)
            print(details)
        except:
            print("error loading page")
    driver.quit()

    with open(output_filename, "w") as json_file:
        json.dump(detail_list, json_file, indent=4)


if __name__ == "__main__":
    link_file = "data/scraped_links.txt"
    data_file = "data/scraped_data.json"

    get_links(link_file)
    get_details(link_file, data_file)

    print("Data gathering completed.")
