from selenium import webdriver
from src.base.playvs_scraper import scrape
import pickle


FIREFOX_PATH = r'drivers/geckodriver'
CHROME_PATH = r'drivers/chromedriver'

FIREFOX = 'Firefox'
CHROME = 'Chrome'

# TODO: Fix error with Chrome on line 67 in playvs_scraper -> invalid XPATH
browser = FIREFOX
teams_to_scrape = ['Saber Smash']

# Set to True to run the scraper, False to just use the cached data.
rescrape = False

if __name__ == '__main__':
    if rescrape:
        if browser == FIREFOX:
            driver = webdriver.Firefox(FIREFOX_PATH)
        elif browser == CHROME:
            driver = webdriver.Chrome(CHROME_PATH)
        else:
            driver = webdriver.Firefox(FIREFOX_PATH)
        teams = scrape(driver, teams_to_scrape.copy())
        pickle.dump(teams, open('archived_teams', 'wb'))
    else:
        teams = pickle.load(open('archived_teams', 'rb'))

    for team_name in teams_to_scrape:
        team = teams[team_name]
        for player in team.players.values():
            player.stats()
            print()
