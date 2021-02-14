from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint

ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.70280045644672%2C%22north%22%3A37.84662702185581%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(
    url=ZILLOW_URL,
    headers=headers
)

FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLScRfjO3mj1s-J3XiQEXILHl-EPChslwcyAERMzMTUEDtUPjqg/viewform?usp=sf_link'
soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())

# Finds all links
all_link_elements = soup.select(".list-card-top a")
links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        links.append(f"https://zillow.com{href}")
    else:
        links.append(href)

# Finds all addresses
address_elements = soup.select("address", class_="list-card-addr")
addresses = [address.text.replace(" | ", ", ") for address in address_elements]

# Finds all prices
all_price_elements = soup.find_all("div", class_="list-card-heading")
prices = []
for element in all_price_elements:
    # Get the prices. Single and multiple listings have different tag & class structures
    try:
        price = element.select(".list-card-price")[0].contents[0]
    except IndexError:
        print("Multiple listings for the card")
        # Price with multiple listings
        price = element.select(".list-card-details li")[0].contents[0]
    finally:
        prices.append(price.replace("+", ""))

chrome_driver_path = "C:/Development/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(
    "https://docs.google.com/forms/d/e/1FAIpQLScRfjO3mj1s-J3XiQEXILHl-EPChslwcyAERMzMTUEDtUPjqg/viewform?vc=0&c=0&w=1&flr=0&gxids=7628")

randsleep = randint(3, 7)
for i in range(len(links)):
    # For the length of list, fill out form questions using list elements
    # First is address, then price, then link to property
    sleep(randsleep)
    address_question = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_question.send_keys(addresses[i])
    price_question = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_question.send_keys(prices[i])
    sleep(randsleep)
    link_question = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_question.send_keys(links[i])
    sleep(randsleep)
    submit_btn = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    submit_btn.click()
    sleep(randsleep)
    another_submit = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_submit.click()
