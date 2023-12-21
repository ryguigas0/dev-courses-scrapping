from ..models.course import Course


def scrap_course(course_soup):
    course = Course(
        image_url=parse_img_url(course_soup),
        complete_time_seconds=parse_time(course_soup),
    )

    return course


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
