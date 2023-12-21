# from .extract_course import scrap_course_page
from .find_courses import scrap_courses
from .extract_course import scrap_course
import logging

logger = logging.getLogger("webscrapping")


def scrap():
    logger.info("STARTED YOUTUBE SCRAPPING")
    courses = list(map(scrap_course, scrap_courses()))

    logger.info("FINISHED YOUTUBE SCRAPPING")

    return courses
