from .extract_course import scrap_course_page
from .find_courses import scrap_course_urls
import logging

logger = logging.getLogger("webscrapping")


def scrap():
    logger.info("STARTED UDEMY SCRAPPING")
    courses = list(map(scrap_course_page, scrap_course_urls()))

    # # Backup json for development
    # with open(f"udemy_scrapping_{datetime.now()}.json", "w") as backup:
    #     json.dump(courses, backup, sort_keys=True, indent=4)

    logger.info("FINISHED UDEMY SCRAPPING")

    return courses
