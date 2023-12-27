from datetime import datetime
from typing import List


class Course:
    def __init__(
        self,
        name: str,
        source_url: str,
        image_url: str,
        rating: float,
        complete_time_seconds: int,
        topic: str,
        languages: List[str],
        instructors: List[str],
        qty_students: int,
        qty_reviews: int,
        updated_at: datetime.date,
        price: float = 0,
    ):
        self.name = name
        self.source_url = source_url
        self.image_url = image_url
        self.rating = rating
        self.complete_time_seconds = complete_time_seconds
        self.topic = topic
        self.languages = languages
        self.instructors = instructors
        self.qty_students = qty_students
        self.qty_reviews = qty_reviews
        self.price = price
        self.updated_at = updated_at
        self.scraped_at = datetime.now()
