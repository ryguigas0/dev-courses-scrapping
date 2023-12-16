from .extract_course import scrap_course_page
from .find_courses import scrap_course_urls


def scrap():
    print(list(map(scrap_course_page, scrap_course_urls())))
