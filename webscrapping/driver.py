import time
import random
import logging
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from .config import FIREFOX_DRIVER, CHROME_DRIVER, USER_AGENTS


logger = logging.getLogger("webscrapping")


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


# DEPRECATED, no need to forge headers
def generate_header_interceptor():
    headers = generate_driver_headers()

    def header_inteceptor(request):
        for header_key in dict.keys(headers):
            del request.headers[header_key]
            request.headers[header_key] = headers[header_key]

    return header_inteceptor


def gen_firefox_driver(proxy):
    logger.info("Using firefox webdriver")

    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0")

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1366,768")

    service = Service(FIREFOX_DRIVER)

    if not proxy is None:
        proxy = Proxy(
            {
                "proxyType": ProxyType.MANUAL,
                "httpProxy": proxy,
            }
        )
        return webdriver.Firefox(
            options=options, service=service, proxy=proxy, firefox_profile=profile
        )

    return webdriver.Firefox(options=options, service=service, firefox_profile=profile)


def gen_chrome_driver(proxy):
    logger.info(f"Using chrome webdriver")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    if not proxy is None:
        options.add_argument("--proxy-server=%s" % proxy)
    options.add_argument("--window-size=1366,768")
    options.add_argument("--mute-audio")

    return webdriver.Chrome(CHROME_DRIVER, options=options)


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
    driver, selector, url=None, single=True, load_wait=3, screenshot=False
):
    return find_element(
        driver, url, By.CSS_SELECTOR, selector, single, load_wait, screenshot
    )


def find_element_by_xpath(
    driver, xpath, url=None, single=True, load_wait=3, screenshot=False
):
    return find_element(driver, url, By.XPATH, xpath, single, load_wait, screenshot)


def find_element(driver, url, by, select_str, single, load_wait, screenshot):
    if not url is None:
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
        return list(
            map(
                lambda w: BeautifulSoup(w.get_attribute("outerHTML"), "lxml"),
                web_element,
            )
        )
    else:
        return BeautifulSoup(web_element.get_attribute("outerHTML"), "lxml")
