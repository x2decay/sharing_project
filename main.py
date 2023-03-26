from selenium import webdriver
from src.base.playvs_scraper import scrape


FIREFOX_PATH = r'drivers/geckodriver'
CHROME_PATH = r'drivers/chromedriver'

FIREFOX = 'Firefox'
CHROME = 'Chrome'

# TODO: Fix error with Chrome on line 69 in playvs_scraper -> invalid XPATH
browser = FIREFOX
teams_to_scrape = ['Bad Decisions']

if __name__ == '__main__':
    if browser == FIREFOX:
        scrape(webdriver.Firefox(FIREFOX_PATH), teams_to_scrape)
    elif browser == CHROME:
        scrape(webdriver.Chrome(CHROME_PATH), teams_to_scrape)
