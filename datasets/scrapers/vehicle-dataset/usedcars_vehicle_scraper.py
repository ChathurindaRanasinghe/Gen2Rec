import json
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WEBSITE_URL = 'https://www.usedcars.com'
# PARAMS = ['/buy']
PARAMS = ['/buy/bodyTypes-convertible',
          '/buy/bodyTypes-coupe',
          '/buy/bodyTypes-hatchback',
          '/buy/bodyTypes-minivan',
          '/buy/bodyTypes-sedan',
          '/buy/bodyTypes-suv',
          '/buy/bodyTypes-truck',
          '/buy/bodyTypes-van',
          '/buy/bodyTypes-wagon']
DRIVER_PATH = 'D:/Inbox/project-Gen2Rec/chromedriver-win64/chromedriver.exe'


def get_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    return webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)


def get_content(driver: WebDriver, param: str, level: int) -> str:
    print(WEBSITE_URL + param)
    driver.get(WEBSITE_URL + param)
    sleep(10)
    for x in range(0, level):
        print('level ' + str(x + 1))
        button = None
        while not button:
            driver.execute_script("window.scrollBy(0, 500);")
            sleep(1)
            try:
                button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "sc-bb59fb03-5"))
                )
                print("Button found")
                break
            except:
                print("Button not found")
        try:
            button.click()
            print("Button clicked")
        except:
            driver.execute_script("window.scrollBy(0, -1000);")
        sleep(5)
        vehicle_links = scrape_links(driver.page_source)
        save_links(vehicle_links)
    return driver.page_source


def scrape_links(content: str) -> list:
    soup = BeautifulSoup(content, 'html.parser')
    vehicle_elements = soup.find_all('a', {'class': 'sc-5a680332-4 jEbBWJ'})
    vehicle_links = [element['href'] for element in vehicle_elements]
    print("number 0f vehicles: " + str(len(vehicle_links)))
    return vehicle_links


def save_links(vehicle_links: list) -> None:
    with open("data/scraped_links" + ".txt", "w") as file:
        for link in vehicle_links:
            file.write(link + '\n')


def get_links() -> None:
    driver = get_driver()
    content = None
    for param in PARAMS:
        content = get_content(driver, param, level=20)
    vehicle_links = scrape_links(content)
    save_links(vehicle_links)
    driver.quit()


def read_links() -> list:
    vehicle_links = []
    with open('data/scraped_links.txt', 'r') as file:
        for line in file:
            vehicle_links.append(line.strip())
    return vehicle_links


def scrape_details(soup: BeautifulSoup) -> dict:
    try:
        details = {
            "name": soup.find('h1', {'class': 'sc-62e5a65e-0 kWFIdk'}).text.strip(),
            "price": soup.find('p', {'class': 'sc-35cccf38-16 lijBWx'}).text.strip(),
            "overview": [span.text.strip() for span in soup.find_all('span', {'class': 'sc-d13ff064-4 jXiDwC'})],
            "features": [span.text.strip() for span in soup.find_all('span', {'class': 'sc-11aa6444-3 edIwFs'})],
            "history": [span.text.strip() for span in soup.find_all('div', {'class': 'sc-8f7178d0-9 lfhAiN'})],
            "seller_notes": soup.find('span', {'id': 'seller-notes-text'}).text.strip(),
            "seller": soup.find('h3', {'class': 'sc-5880c977-3 egrhEm'}).text.strip()
        }
        if soup.find('div', {'class': 'sc-f4e7e306-2 iFfVqN'}):
            details["review"] = soup.find('div', {'class': 'sc-f4e7e306-2 iFfVqN'}).text.strip()
        return details
    except:
        print("error scraping details")


def get_details() -> None:
    links = read_links()
    detail_list = []
    driver = get_driver()
    for link in links:
        try:
            driver.get(WEBSITE_URL + link)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            details = scrape_details(soup)
            detail_list.append(details)
            print(details)
        except:
            print("error loading page")
    driver.quit()

    with open("data/scraped_data.json", 'w') as json_file:
        json.dump(detail_list, json_file, indent=4)


if __name__ == "__main__":
    get_links()
    # get_details()
