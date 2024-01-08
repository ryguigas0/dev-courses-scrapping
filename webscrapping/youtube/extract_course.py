from ...models.course import Course, insert_course
from ...models.language import Language
from ...models.instructor import Instructor
from ..config import YT_ROOT_URL, YT_COMMENT_XPATH, YT_LIKES_PATH, YT_VIEWS_PATH
from ..driver import generate_driver, find_element_by_xpath
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger("webscrapping")


def scrap_course(course_soup, lang, topic):
    try:
        source_url = parse_source_url(course_soup)
        (rating, qty_students, qty_reviews) = calc_rating(source_url)

        course = Course(
            name=parse_course_name(course_soup),
            source_url=source_url,
            image_url=parse_img_url(course_soup),
            complete_time_seconds=parse_time(course_soup),
            topic=topic,
            languages=parse_language(lang),
            instructors=parse_instructors(course_soup),
            qty_students=qty_students,
            qty_reviews=qty_reviews,
            rating=rating,
            updated_at=parse_last_update_date(course_soup),
        )

        return insert_course(course)
    except Exception as e:
        logger.error(f"{str(type(e))} {str(e)}")
        return


def parse_language(lang):
    return [Language(name=lang)]


def parse_last_update_date(course_soup):
    label = course_soup.select("#video-title > yt-formatted-string")[0]["aria-label"]

    (str_num, unit) = re.findall(r"(\d+) (minute|hour|day|week|month|year)", label)[0]

    num = int(str_num)

    kwargs_timedelta = {}
    if unit == "year":
        kwargs_timedelta["days"] = num * 365
    elif unit == "month":
        kwargs_timedelta["days"] = num * 30
    else:
        kwargs_timedelta[unit + "s"] = num

    return datetime.now() - timedelta(**kwargs_timedelta)


def calc_rating(source_url):
    driver = generate_driver(has_proxy=False)

    # qty_review = int(
    #     find_element_by_xpath(driver, YT_COMMENT_XPATH, url=source_url).get_attribute(
    #         "innerText"
    #     )
    # )

    views_tooltip = find_element_by_xpath(
        driver, YT_VIEWS_PATH, url=source_url
    ).get_attribute("innerText")

    qty_students = int(
        re.findall("(\d{1,3}(?:\,\d{3})*)", views_tooltip)[0].replace(",", "")
    )

    likes_msg = find_element_by_xpath(driver, YT_LIKES_PATH).get_attribute("aria-label")

    qty_review = int(re.findall("(\d{1,3}(?:\,\d{3})*)", likes_msg)[0].replace(",", ""))

    rating = qty_review / qty_students * 5

    return (rating, qty_students, qty_review)


def parse_instructors(course_soup):
    name = course_soup.select("#text > a")[0].get_text()
    return [Instructor(name=name)]


def parse_source_url(course_soup):
    return YT_ROOT_URL + course_soup.select("#video-title")[0].get("href")


def parse_course_name(course_soup):
    return course_soup.select("#video-title")[0].get_text().strip()


def parse_img_url(course_soup):
    return course_soup.select("#thumbnail > yt-image > img")[0]["src"]


def parse_time(course_soup):
    time_html = course_soup.find(
        "span",
        {
            "id": "text",
            "class": "style-scope ytd-thumbnail-overlay-time-status-renderer",
        },
    )

    time_split = time_html.get_text().strip().split(":")

    mult = 1

    time_seconds = 0

    while len(time_split) > 0:
        n = int(time_split.pop())

        time_seconds += n * mult

        mult *= 60

    return time_seconds
