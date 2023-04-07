import src.base.json_conversion as json
from src.base.playvs_scraper import *
from selenium import webdriver
import pickle

teams_to_scrape = ['ThunderRidge Green Team']

# Set to True to run the scraper, False to just use the cached data.
scrape_players = True
# Leave on False unless you want to scrape a different team
scrape_teams = False

if __name__ == '__main__':
    teams = pickle.load(open('archived_teams', 'rb'))
    # with open('example.json', 'r') as file:
    #     teams = json.to_classes(file)
    if scrape_players or scrape_teams:
        driver = webdriver.Firefox(r'drivers/geckodriver')
        start_scraper(driver)
        if scrape_teams:
            # noinspection PyRedeclaration
            teams = team_scraper(driver, teams_to_scrape)
        if scrape_players:
            actions = webdriver.ActionChains(driver)
            # noinspection PyUnboundLocalVariable
            teams = player_scraper(driver, actions, teams)
            pickle.dump(teams, open('archived_teams', 'wb'))
        else:
            pass
        driver.quit()
    for (team_name, team) in teams.items():
        print(team_name)
        for (player_name, player) in team.players.items():
            print(player_name)
            player.print_stats()
