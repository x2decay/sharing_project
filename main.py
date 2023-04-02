from selenium import webdriver
from selenium.webdriver import ActionChains
from src.base.playvs_scraper import *
import src.base.jsons
import pickle

teams_to_scrape = ['ThunderRidge Green Team']

# Set to True to run the scraper, False to just use the cached data.
scrape_players = False
# Leave on False unless you want to scrape a different team
scrape_teams = False


if __name__ == '__main__':
    teams = pickle.load(open('archived_teams', 'rb'))
    with open('example.json', 'r') as file:
        teams = jsons.to_classes(file)
    print(j)
    if scrape_players or scrape_teams:
        driver = webdriver.Firefox(r'drivers/geckodriver')
        start_scraper(driver)
        if scrape_teams:
            teams = team_scraper(driver, teams_to_scrape)
        else:
            pass
        if scrape_players:
            actions = webdriver.ActionChains(driver)
            teams = player_scraper(driver, teams, actions)
            pickle.dump(teams, open('archived_teams', 'wb'))
        else:
            pass
        driver.quit()
    for team in teams.values():
        print(team.name)
        for player in team.players.values():
            player.print_stats()
            print()
