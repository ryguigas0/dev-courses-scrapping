import time
from ..driver import generate_driver, find_element_by_selector
import logging
import random
from ..config import UDEMY_TOPICS, UDEMY_COURSE_ANCHORS_SELECTOR, WAIT_TIME

logger = logging.getLogger("webscrapping")


def scrap_course_urls():
    logger.info("Gattering courses urls")
    random.shuffle(UDEMY_TOPICS)
    courses_urls = []

    t = UDEMY_TOPICS[0]

    logger.info(f"Scrapping topic '{t[2]}'...")

    wait = random.randint(WAIT_TIME, WAIT_TIME + 30)

    logger.info(f"Waiting {wait}s before topic load...")

    time.sleep(wait)

    driver = generate_driver()

    logger.info(f"Loading topic...")

    course_anchors = find_element_by_selector(
        driver,
        t[0],
        UDEMY_COURSE_ANCHORS_SELECTOR,
        single=False,
        load_wait=8,
    )

    courses_urls_found = list(
        map(
            lambda el: el.get_attribute("href"),
            course_anchors,
        )
    )

    logger.info(f"Yielded {len(courses_urls_found)} courses!")

    courses_urls.extend(courses_urls_found)

    driver.quit()

    logger.info("Finished courses urls")

    return courses_urls
