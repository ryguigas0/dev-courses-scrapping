import time
import random
import logging
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


logger = logging.getLogger("webscrapping")

USER_AGENTS = [
    # windows 10 edge
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    },
    # chromeOS chrome
    {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Sec-Ch-Ua-Platform": '"Chrome OS"',
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    },
    # macOS safari
    # {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    #     "Sec-Ch-Ua-Platform": '"macOS"',
    #     "Sec-Ch-Ua": 'Sec-Ch-Ua: "Safari";v="17", " Not A Brand";v="99"',
    # },
    # Windows 7 chrome
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua": '"Google Chrome";v="109", "Chromium";v="109", ";Not A Brand";v="8"',
    },
    # Linux firefox
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        # "Sec-Ch-Ua": '"Google Chrome";v="120", "Chromium";v="120", ";Not A Brand";v="8"',
    },
]


def generate_driver_headers():
    curr_device_headers = random_from_list(USER_AGENTS)
    logger.info(f'using agent {curr_device_headers["Sec-Ch-Ua-Platform"]}')

    default_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en",
        # "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        # "Upgrade-Insecure-Requests": "1",
        # "X-Amzn-Trace-Id": "Root=1-658091af-0e89637646691d4a60504ea6",
    }

    default_headers.update(curr_device_headers)

    return default_headers


def generate_header_interceptor():
    headers = generate_driver_headers()

    def header_inteceptor(request):
        for header_key in dict.keys(headers):
            del request.headers[header_key]
            request.headers[header_key] = headers[header_key]

    return header_inteceptor


def gen_firefox_driver(proxy):
    logger.info("Using firefox webdriver")

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1366,768")

    service = Service(GeckoDriverManager().install())

    if not proxy is None:
        proxy = Proxy(
            {
                "proxyType": ProxyType.MANUAL,
                "httpProxy": proxy,
            }
        )
        return webdriver.Firefox(options=options, service=service, proxy=proxy)

    return webdriver.Firefox(options=options, service=service)


def gen_chrome_driver(proxy):
    logger.info(f"Using chrome webdriver")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    if not proxy is None:
        options.add_argument("--proxy-server=%s" % proxy)
    options.add_argument("--window-size=1366,768")

    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


def generate_driver(has_proxy=True):
    proxy_ip = None
    if has_proxy:
        from .proxy import proxy_list

        proxy_ip = random_from_list(proxy_list)["URL"]

    logger.info(f"Using proxy {proxy_ip}")

    driver_generators = [gen_chrome_driver, gen_firefox_driver]

    driver = random_from_list(driver_generators)(proxy_ip)

    # driver.request_interceptor = generate_header_interceptor()

    return driver


def random_from_list(list):
    index_chosen = random.randint(0, len(list) - 1)
    return list[index_chosen]


def find_element_by_selector(
    driver, url, selector, single=True, load_wait=3, screenshot=False
):
    return find_element(
        driver, url, By.CSS_SELECTOR, selector, single, load_wait, screenshot
    )


def find_element_by_xpath(
    driver, url, xpath, single=True, load_wait=3, screenshot=False
):
    return find_element(driver, url, By.XPATH, xpath, single, load_wait, screenshot)


def find_element(driver, url, by, select_str, single, load_wait, screenshot):
    driver.get(url)

    logger.info(f"Loading page...")

    time.sleep(load_wait)

    if screenshot:
        if driver.get_screenshot_as_file(f"Screenshot{datetime.now()}.png"):
            logger.info(f"Screenshoted page")
        else:
            logger.info(f"Screenshot error!")

    if single:
        return driver.find_element(by, select_str)
    else:
        return driver.find_elements(by, select_str)


def soupfy(web_element):
    logger.info("Soupfying content")
    if type(web_element) is list:
        return list(map(lambda w: BeautifulSoup(w.get_attribute("outerHTML"), "lxml"), web_element))
    else:
        return BeautifulSoup(web_element.get_attribute("outerHTML"), "lxml")
