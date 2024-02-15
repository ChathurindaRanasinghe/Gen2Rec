from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.usedcars.com'
arguments = '/buy'
path = 'D:/Inbox/project-Gen2Rec/chromedriver-win64/chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

driver.get(url + arguments)
sleep(10)

for x in range(0, 200):
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
            print("Button not found yet")

    try:
        button.click()
        print("Button clicked")
    except:
        driver.execute_script("window.scrollBy(0, -1000);")
    sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    vehicle_elements = soup.find_all('a', {'class': 'sc-5a680332-4 jEbBWJ'})

    vehicle_links = [element['href'] for element in vehicle_elements]
    print(len(vehicle_links))
    with open("data/scraped_links" + ".txt", "w") as file:
        for link in vehicle_links:
            file.write(link + '\n')

# content = driver.page_source
driver.quit()

# soup = BeautifulSoup(content, 'html.parser')
# vehicle_elements = soup.find_all('a', {'class': 'sc-5a680332-4 jEbBWJ'})
#
# vehicle_links = [element['href'] for element in vehicle_elements]
# print(len(vehicle_links))
# with open("data/scraped_links.txt", "w") as file:
#     for link in vehicle_links:
#         file.write(link + '\n')
