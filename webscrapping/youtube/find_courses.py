import logging
import random
from ..config import UDEMY_TOPICS, YT_COURSES_XPATH
from ..driver import generate_driver, find_element_by_xpath, soupfy

logger = logging.getLogger("webscrapping")


def scrap_courses():
    random.shuffle(UDEMY_TOPICS)

    scrapped_courses = {}

    for t in UDEMY_TOPICS:
        logger.info(f"Scrapping topic '{t[2]}'...")

        driver = generate_driver(has_proxy=False)

        topic_query = t[2].replace("+", "%2B").replace(" ", "+")

        url = f"https://www.youtube.com/results?search_query={topic_query}&sp=EgIYAg%253D%253D"

        language = find_element_by_xpath(
            driver=driver,
            url=url,
            xpath="/html",
        ).get_attribute("lang")

        courses = soupfy(
            find_element_by_xpath(driver, YT_COURSES_XPATH, single=False, load_wait=0)
        )

        logger.info(f"Yielded {len(courses)} courses!")

        scrapped_courses[t[2]] = (language, courses)

        driver.quit()

    logger.info("Finished courses urls")

    return scrapped_courses
