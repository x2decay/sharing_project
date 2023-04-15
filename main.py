import src.base.json_conversion as json
from src.base.playvs_scraper import *
from selenium import webdriver
import pickle

team_name = 'RMHS Lobos Varsity C'

# Leave on False unless you want to scrape a different team
scrape_team = False
# Set to True to run the scraper, False to just use the cached data.
scrape_players = False

if __name__ == '__main__':
    team = pickle.load(open('archived_teams', 'rb'))
    # with open('example.json', 'r') as file:
    #     team = json.to_classes(file)
    if scrape_players or scrape_team:
        driver = webdriver.Firefox(r'drivers/geckodriver')
        start_scraper(driver)
        if scrape_team:
            # noinspection PyRedeclaration
            team = team_scraper(driver, team_name)
        if scrape_players:
            actions = webdriver.ActionChains(driver)
            # noinspection PyUnboundLocalVariable
            team = player_scraper(driver, actions, team)
        pickle.dump(team, open('archived_teams', 'wb'))
        driver.quit()
    print(team_name)
    for player in team.players:
        print(player.name)
        player.print_stats()
