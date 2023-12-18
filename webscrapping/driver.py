import time
import random
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


logger = logging.getLogger("webscrapping")


def header_inteceptor(request):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en",
        "Host": "httpbin.org",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # "X-Amzn-Trace-Id": "Root=1-658091af-0e89637646691d4a60504ea6",
    }

    for key in dict.keys(headers):
        del request.headers[key]
        request.headers[key] = headers[key]


def gen_firefox_driver():
    logger.info("Using firefox webdriver")

    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")

    service = Service(GeckoDriverManager().install())

    return webdriver.Firefox(options=options, service=service)


def gen_chrome_driver():
    logger.info("Using chrome webdriver")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    service = Service(ChromeDriverManager.install())

    return webdriver.Chrome(options=options, service=service)


def generate_driver():
    driver_generators = [gen_firefox_driver, gen_chrome_driver]
    index_chosen = random.randint(0, len(driver_generators) - 1)
    return driver_generators[index_chosen]()


def find_element(driver, url, xpath, single=True, load_wait=3, screenshot=False):
    driver.get(url)

    logger.info(f"Loading page...")

    time.sleep(load_wait)

    if screenshot:
        if driver.get_screenshot_as_file(f"Screenshot{datetime.now()}.png"):
            logger.info(f"Screenshoted page")
        else:
            logger.info(f"Screenshot error!")

    logger.info("Scrapping page")

    if single:
        return driver.find_element(By.XPATH, xpath)
    else:
        return driver.find_elements(By.XPATH, xpath)


def soupfy(web_element):
    logger.info("Soupfying content")
    if web_element is list:
        return list(map(lambda w: BeautifulSoup(w.get_attribute("outerHTML"), "lxml")))
    else:
        return BeautifulSoup(web_element.get_attribute("outerHTML"), "lxml")
