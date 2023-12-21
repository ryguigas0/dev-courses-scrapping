import logging
import random
from ..config import UDEMY_TOPICS, YOUTUBE_COURSES_XPATH
from ..driver import generate_driver, find_element_by_xpath, soupfy

logger = logging.getLogger("webscrapping")


def scrap_courses():
    random.shuffle(UDEMY_TOPICS)

    t = UDEMY_TOPICS[0]

    logger.info(f"Scrapping topic '{t[2]}'...")

    driver = generate_driver(has_proxy=False)

    topic_query = t[2].replace("+", "%2B").replace(" ", "+")

    url = f"https://www.youtube.com/results?search_query={topic_query}&sp=EgIYAg%253D%253D"

    courses = soupfy(
        find_element_by_xpath(
            driver, url, YOUTUBE_COURSES_XPATH, single=False, screenshot=True
        )
    )

    logger.info(f"Yielded {len(courses)} courses!")

    driver.quit()

    logger.info("Finished courses urls")

    return courses
