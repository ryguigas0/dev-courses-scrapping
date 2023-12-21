import logging
import json
from datetime import datetime

logger = logging.getLogger("webscrapping")
logger.setLevel(logging.INFO)

# log file
fh = logging.FileHandler(f"webscrapping{datetime.now()}.log", "w")
fh.setLevel(logging.INFO)

# Console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(module)s - %(message)s")
fh.setFormatter(fmt)

logger.addHandler(ch)
logger.addHandler(fh)

from .udemy import scrap as udemy_scrapping
from .youtube import scrap as youtube_scrapping

scrappings = [youtube_scrapping, udemy_scrapping]
courses = []

for scrap in scrappings:
    courses.extend(scrap())

# Backup json for development
with open(f"webscrapping_output{datetime.now()}.json", "w") as backup:
    json.dump(courses, backup, sort_keys=True, indent=4)
