from selenium import webdriver
from src.base.playvs_scraper import scrape


FIREFOX_PATH = r'drivers/geckodriver'
CHROME_PATH = r'drivers/chromedriver'

FIREFOX = 'Firefox'
CHROME = 'Chrome'
browsers = [FIREFOX, CHROME]

# TODO: Fix error with Chrome on line 67 in playvs_scraper -> invalid XPATH
browser = FIREFOX
teams_to_scrape = ['Bad Decisions']

if __name__ == '__main__':
    if browser == FIREFOX:
        driver = webdriver.Firefox(FIREFOX_PATH)
    elif browser == CHROME:
        driver = webdriver.Chrome(CHROME_PATH)
    else:
        driver = webdriver.Firefox(FIREFOX_PATH)

    teams = scrape(driver, teams_to_scrape.copy())

    print(teams_to_scrape)

    for team_name in teams_to_scrape:
        team = teams[team_name]
        for player in team.players.values():
            print(player.name)
            player.characters()
