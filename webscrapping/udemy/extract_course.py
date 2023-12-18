import json
from ..driver import get_soup_from_page
import logging

logger = logging.getLogger("webscrapping")

UDEMY_DATA_XPATH = '//*[@id="br"]/div[1]/div[2]/div/div'
# Udemy doesent load course content when scrapping
# UDEMY_CONTENT_XPATH = '//*[@id="main-content-anchor"]/div[5]/div/div[4]/div/div[2]/div/div/div/ul/li/div'


def scrap_course_page(course_url):
    logger.info(f"Scrapping course {course_url}")
    udemy_data_json = json.loads(
        get_soup_from_page(course_url, UDEMY_DATA_XPATH).div["data-component-props"]
    )["serverSideProps"]

    # # Backup json for development
    # with open(f"{udemy_data_json['course']['id']}.json", "w") as backup:
    #     json.dump(udemy_data_json, backup, sort_keys=True, indent=4)

    logger.info(f"Finished scrapping course {course_url}")

    return course_json2dict(udemy_data_json)


def course_json2dict(udemy_json):
    return {
        "source_url": udemy_json["course"]["url"],
        "image": udemy_json["introductionAsset"]["images"]["image_480x270"],
        "name": udemy_json["course"]["title"],
        "rating": udemy_json["course"]["rating"],
        "complete_time_seconds": udemy_json["course"]["contentLengthVideo"],
        "topic": parse_topics(udemy_json["topicMenu"]["breadcrumbs"]),
        "languages": parse_languages(udemy_json["course"]["captionedLanguages"]),
        "instructors": parse_instructors(
            udemy_json["course"]["instructors"]["instructors_info"]
        ),
        "qty_students": udemy_json["course"]["numStudents"],
        "qty_reviews": udemy_json["course"]["numReviews"],
        "updated_at": udemy_json["course"]["lastUpdateDate"],
        "price": parse_price(udemy_json),
        # "price_discount": "",
    }


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
