import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.add_argument("-headless")


def create_driver(url=None, load_time=3):
    driver = webdriver.Firefox(options=options)

    if not url is None:
        driver.get(url)
        time.sleep(load_time)

    return driver


def find_element_by_xpath(driver, xpath, single=True):
    return (
        driver.find_element(By.XPATH, xpath)
        if single
        else driver.find_elements(By.XPATH, xpath)
    )


def get_soups_from_page(url, xpath, wait=3):
    driver = webdriver.Firefox(options=options)

    driver.get(url)

    time.sleep(wait)

    soups = list(
        map(
            lambda e: BeautifulSoup(
                e.get_attribute("outerHTML"),
                "lxml",
            ),
            driver.find_elements(By.XPATH, xpath),
        )
    )

    driver.quit()

    return soups


def get_soup_from_page(url, xpath, wait=3):
    driver = webdriver.Firefox(options=options)

    driver.get(url)

    time.sleep(wait)

    soup = BeautifulSoup(
        driver.find_element(By.XPATH, xpath).get_attribute("outerHTML"),
        "lxml",
    )

    driver.quit()

    return soup
