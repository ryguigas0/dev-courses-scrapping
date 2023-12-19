import logging

logger = logging.getLogger("webscrapping")
logger.setLevel(logging.INFO)

# log file
fh = logging.FileHandler("webscrapping.log", "w")
fh.setLevel(logging.INFO)

# Console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(module)s - %(message)s")
fh.setFormatter(fmt)

logger.addHandler(ch)
logger.addHandler(fh)

from .udemy import scrap as udemy_scrapping

udemy_scrapping()
