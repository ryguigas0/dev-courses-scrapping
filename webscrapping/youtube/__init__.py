# from .extract_course import scrap_course_page
from .find_courses import scrap_courses
from .extract_course import scrap_course
import logging

logger = logging.getLogger("webscrapping")


def scrap():
    logger.info("STARTED YT SCRAPPING")

    scrapped_courses = scrap_courses()
    for topic_key in scrapped_courses:
        (lang, courses) = scrapped_courses[topic_key]

        list(map(lambda c: scrap_course(c, lang, topic_key), courses))

    logger.info("FINISHED YT SCRAPPING")

    return courses
