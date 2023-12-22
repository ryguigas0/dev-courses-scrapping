# Developer courses webscrapping

Udemy and Youtube developer courses webscrapper and API

- Scrapped topics are in `webscrapping/config.py`
- Proxy server list used are in `proxy_list.txt` (sources: [free proxy list](https://free-proxy-list.net/), [hidemy.io](https://hidemy.io/en/proxy-list/countries/brazil/), [proxynova](https://www.proxynova.com/proxy-server-list/country-br/))

## Running the project

DISCLAIMER: Udemy scrapping is current not working and not being used

### Requirements

- Python 3.8 or greater
- Google Chrome 120 or greater ([how to install on ubuntu](https://www.xda-developers.com/how-install-chrome-ubuntu/))
- Firefox 121 or greater ([how to install on ubuntu](https://linuxconfig.org/how-to-install-uninstall-and-update-firefox-on-ubuntu-20-04-focal-fossa-linux))

### Webscrapper

1. Clone the project
2. Install the dependencies: `pip3 install -r requirements.txt`
3. `python3 -m webscrapping`

- Generated log file name: `webscrapping{timestamp}.log` (Ex.: `webscrapping2023-12-20 11:00:37.785045.log`
- Page screenshot file name: `Screenshot{timestamp}.png` (Ex.: `Screenshot2023-12-20 11:11:51.529082.png`)
