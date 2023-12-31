import json
from ..driver import generate_driver, soupfy, find_element_by_xpath
import logging
import time
import random
from ..config import WAIT_TIME, UDEMY_COURSE_SCHEMA_XPATH
from ...models import Course

logger = logging.getLogger("webscrapping")

# Udemy doesent load course content when scrapping
# UDEMY_CONTENT_XPATH = '//*[@id="main-content-anchor"]/div[5]/div/div[4]/div/div[2]/div/div/div/ul/li/div'


def scrap_course_page(course_url):
    logger.info(f"Scrapping course {course_url}")

    wait = random.randint(WAIT_TIME, WAIT_TIME + 100)

    logger.info(f"Waiting {wait}s before course load...")

    time.sleep(wait)

    driver = generate_driver()

    udemy_schema = soupfy(
        find_element_by_xpath(
            driver, course_url, UDEMY_COURSE_SCHEMA_XPATH, screenshot=True
        )
    ).div["data-component-props"]

    driver.quit()

    udemy_data_json = json.loads(udemy_schema)["serverSideProps"]

    # # Backup json for development
    # with open(f"{udemy_data_json['course']['id']}.json", "w") as backup:
    #     json.dump(udemy_data_json, backup, sort_keys=True, indent=4)

    logger.info(f"Finished scrapping course {course_url}")

    return course_json2dict(udemy_data_json)


def course_json2dict(udemy_json):
    return Course(
        name=udemy_json["course"]["title"],
        source_url=udemy_json["course"]["url"],
        image_url=udemy_json["introductionAsset"]["images"]["image_480x270"],
        rating=udemy_json["course"]["rating"],
        complete_time_seconds=udemy_json["course"]["contentLengthVideo"],
        topic=parse_topics(udemy_json["topicMenu"]["breadcrumbs"]),
        languages=parse_languages(udemy_json["course"]["captionedLanguages"]),
        instructors=parse_instructors(
            udemy_json["course"]["instructors"]["instructors_info"]
        ),
        qty_students=udemy_json["course"]["numStudents"],
        qty_reviews=udemy_json["course"]["numReviews"],
        price=parse_price(udemy_json),
    )


def parse_price(udemy_json):
    is_paid = udemy_json["sidebarContainer"]["componentProps"]["purchaseSection"][
        "is_course_paid"
    ]
    if not is_paid:
        return 0

    seo_schema = json.loads(udemy_json["seoInfo"]["schema"])

    return seo_schema[0]["offers"][0]["price"]


def parse_topics(topics_arr):
    return "/".join(list(map(lambda t: t["title"].lower(), topics_arr)))


def parse_languages(languages_arr):
    return ",".join(languages_arr)


def parse_instructors(instructors_arr):
    return list(
        map(
            lambda i: {
                "name": i["display_name"],
                "rating": i["avg_rating_recent"],
                "id": i["absolute_url"],
                "job_title": i["job_title"],
                "image": i["image_75x75"],
            },
            instructors_arr,
        )
    )
