import logging
from datetime import datetime
from ..models import create_database

# DATABASE SETUP
create_database()

# LOGGER SETUP

logger = logging.getLogger("webscrapping")
logger.setLevel(logging.INFO)

# log file
fh = logging.FileHandler(f"webscrapping.log", "a")
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

scrappings = [youtube_scrapping]

for scrap in scrappings:
    scrap()
