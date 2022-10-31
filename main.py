from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"

req_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9 ",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                  "Safari/537.36",
    }

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeGFq5P5ChO2uBz863Ns28yy0ygT3wgawn-nMr-b5qUhuNiRg/viewform?usp" \
           "=sf_link "
zillow_url = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22" \
             "%3A%7B%22west%22%3A-122.56876982641602%2C%22east%22%3A-122.29788817358398%2C%22south%22%3A37" \
             ".666392459969764%2C%22north%22%3A37.88403027709228%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue" \
             "%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C" \
             "%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22" \
             "%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22" \
             "%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22" \
             "%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D "

response = requests.get(zillow_url, headers=req_headers)
zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")

# print(soup.prettify())
listings = soup.find(class_="search-page-container map-on-left")
# print(listings.prettify())

links = listings.find_all(class_="property-card-link")
addresses = listings.find_all('address')
prices = listings.find_all("span", attrs={"data-test": "property-card-price"})


driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(form_url)

for i in range(len(addresses)):
    address = addresses[i].text
    link = links[i].get("href")
    price = prices[i].text

    time.sleep(1)

    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                                  '1]/div/div[1]/input')
    address_input.send_keys(address)

    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                                '1]/div/div[1]/input')
    price_input.send_keys(price)

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    link_input.send_keys(link)

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(2)

    submit_another_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_button.click()

