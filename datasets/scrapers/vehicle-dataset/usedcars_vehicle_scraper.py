from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WEBSITE_URL = 'https://www.usedcars.com'
PARAMS = '/buy'


def get_driver() -> WebDriver:
    path = 'D:/Inbox/project-Gen2Rec/chromedriver-win64/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    return webdriver.Chrome(executable_path=path, chrome_options=chrome_options)


def get_content(driver: WebDriver, level: int) -> str:
    driver.get(WEBSITE_URL + PARAMS)
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


def main() -> None:
    driver = get_driver()
    content = get_content(driver, level=2)
    vehicle_links = scrape_links(content)
    save_links(vehicle_links)
    driver.quit()


if __name__ == "__main__":
    main()
