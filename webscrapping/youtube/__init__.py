# from .extract_course import scrap_course_page
from .find_courses import scrap_courses
from .extract_course import scrap_course
import logging

logger = logging.getLogger("webscrapping")


def scrap():
    logger.info("STARTED YOUTUBE SCRAPPING")

    scrapped_courses = scrap_courses()
    courses = []
    for topic_key in scrapped_courses:
        (lang, courses) = scrapped_courses[topic_key]

        courses.extend(list(map(lambda c: scrap_course(c, lang, topic_key), courses)))

    logger.info("FINISHED YOUTUBE SCRAPPING")

    return courses
