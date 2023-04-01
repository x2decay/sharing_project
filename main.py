from selenium import webdriver
from src.base.playvs_scraper import scrape
import pickle


teams_to_scrape = ['ThunderRidge Green Team']

# Set to True to run the scraper, False to just use the cached data.
rescrape_players = False
# Leave on False unless you want to scrape a different team
rescrape_teams = False

if __name__ == '__main__':
    teams = pickle.load(open('archived_teams', 'rb'))
    if rescrape_players:
        driver = webdriver.Firefox(r'drivers/geckodriver')
        teams = scrape(driver, teams_to_scrape.copy(), teams, rescrape_teams)
        pickle.dump(teams, open('archived_teams', 'wb'))

    for team_name in teams_to_scrape:
        team = teams[team_name]
        for player in team.players.values():
            player.print_stats()
            print()
