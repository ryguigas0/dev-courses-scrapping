from .extract import scrape_course_page


def scrape():
    courses_url = ["https://www.udemy.com/course/100-days-of-code/"]

    print(list(map(scrape_course_page, courses_url)))
