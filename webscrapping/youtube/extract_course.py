from ..models.course import Course
from ..config import YOUTUBE_ROOT_URL


def scrap_course(course_soup, lang, topic):
    qty_students = parse_student_qty(course_soup)

    course = Course(
        name=parse_course_name(course_soup),
        source_url=parse_source_url(course_soup),
        image_url=parse_img_url(course_soup),
        complete_time_seconds=parse_time(course_soup),
        topic=topic,
        languages=[lang],
        instructors=parse_instructors(course_soup),
        qty_students=qty_students
    )

    return course

def parse_instructors(course_soup):
    return [course_soup.select("#text > a")[0].get_text()]


def parse_source_url(course_soup):
    return YOUTUBE_ROOT_URL + course_soup.select("#video-title")[0].get("href")


def parse_course_name(course_soup):
    return course_soup.select("#video-title")[0].get_text().strip()


def parse_img_url(course_soup):
    return course_soup.select("#thumbnail > yt-image > img")[0]["src"]


def parse_time(course_soup):
    time_split = (
        course_soup.find(
            "span",
            {
                "id": "text",
                "class": "style-scope ytd-thumbnail-overlay-time-status-renderer",
            },
        )
        .get_text()
        .strip()
        .split(":")
    )

    mult = 1

    time_seconds = 0

    while len(time_split) > 0:
        n = int(time_split.pop())

        time_seconds += n * mult

        mult *= 60

    return time_seconds
