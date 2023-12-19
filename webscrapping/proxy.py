import requests
import logging

logger = logging.getLogger("webscrapping")

country_list = ["United States"]


def check_proxy(proxy_dict):
    if not proxy_dict["country"] in country_list:
        logger.info(f"Dropping proxy {proxy_dict['URL']}, invalid country")
        return False

    try:
        resp = requests.get(
            "https://ifconfig.me/ip", proxies={"http": proxy_dict["URL"]}, timeout=30
        )

        logger.info(f"Trying proxy {proxy_dict['URL']}, {resp.ok}")

        return resp.ok
    except:
        logger.info(f"Dropping proxy {proxy_dict['URL']}, connection bad")
        return False


def parse2proxy(proxy_str):
    row = proxy_str.split(";")
    return {"URL": f"{row[0]}:{row[1]}", "country": row[2]}


logger.info("Preparing proxy list")
proxy_list = list(
    filter(
        check_proxy,
        map(parse2proxy, open("proxy_list.txt", "r").read().split("\n")),
    )
)
logger.info("Proxy list finished!")
