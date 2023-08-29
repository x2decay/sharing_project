from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.base.playvs_objects import Team
from selenium import webdriver
from unidecode import unidecode
import time

current_season = 'Spring 2023'


def start_scraper(driver):
    url = 'https://app.playvs.com/app/standings'
    with open('login.txt') as file:
        words = str(file).split()
        email = words[words.index('email:') + 1]
        password = words[words.index('password:') + 1]
    driver.get(url)

    # Login
    driver.implicitly_wait(2)
    email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    email_input.send_keys(*list(email))
    password_input.send_keys(*list(password))
    password_input.send_keys(Keys.ENTER)

    # Deny Cookies
    driver.implicitly_wait(5)
    x_button = driver.find_element(By.CSS_SELECTOR, 'button[class="onetrust-close-btn-handler '
                                                    'ot-close-icon banner-close-button"]')
    x_button.click()

    # Switch to Dark Mode
    driver.implicitly_wait(5)
    settings = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="account-settings-navigation"]')
    settings.click()
    driver.implicitly_wait(2)
    dark = driver.find_elements(By.CSS_SELECTOR, 'li[role="menuitem"]')[6]
    dark.click()
    dark.send_keys(Keys.ESCAPE)


def team_scraper(driver, team_name, scrape_season):
    # Switch to Smash
    driver.implicitly_wait(5)
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-cy="Colorado CHSAA League of Legends"]')) > 0:
        league = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Colorado CHSAA League of Legends"]')
        time.sleep(.5)
        league.click()
        driver.implicitly_wait(2)
        smash = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Colorado CHSAA Super Smash Bros.™ Ultimate"]')
        smash.click()

    # Switch to Spring 2023
    driver.implicitly_wait(5)
    if len(driver.find_elements(By.CSS_SELECTOR, f'button[data-cy="{current_season}"]')) > 0:
        season = driver.find_element(By.CSS_SELECTOR, f'button[data-cy="{current_season}"]')
        season.click()
        driver.implicitly_wait(2)
        spring23 = driver.find_element(By.CSS_SELECTOR, f'li[data-cy="{scrape_season}"]')
        spring23.click()

    # Switch to Regular Season
    driver.implicitly_wait(5)
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-cy="Playoffs')) > 0:
        season = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Playoffs"]')
        season.click()
        driver.implicitly_wait(2)
        spring23 = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Regular Season"]')
        spring23.click()

    # Find the team
    team = Team(driver.find_element(By.XPATH, f'//div[a[p[contains(text(), "{team_name}")]]]'))
    return team


def player_scraper(driver, actions, team):
    # Reset players
    team.players = []
    # Opens Team Page
    driver.get(team.href)
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-cy="Fall 2021"')) > 0:
        fall = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Fall 2021"]')
        fall.click()
        driver.implicitly_wait(2)
        spring = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Spring 2023"]')
        spring.click()
    team = match_scraper(driver, actions, team)
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-cy="Playoffs - Semi Finals / Finals')) > 0:
        play = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Playoffs - Semi Finals / Finals"]')
        play.click()
        driver.implicitly_wait(2)
        reg = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Playoffs"]')
        reg.click()
    team = match_scraper(driver, actions, team)
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-cy="Playoffs')) > 0:
        play = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Playoffs"]')
        play.click()
        driver.implicitly_wait(2)
        reg = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Regular Season"]')
        reg.click()
    team = match_scraper(driver, actions, team)
    if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-cy="Regular Season"]')) > 0:
        reg = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Regular Season"]')
        reg.click()
        driver.implicitly_wait(2)
        pre = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Preseason"]')
        pre.click()
    team = match_scraper(driver, actions, team)
    return team


def match_scraper(driver: webdriver, actions, team):
    more = driver.find_elements(By.XPATH, '//div[contains(text(),"Show More")]')
    if len(more) > 0:
        more[0].click()
    driver.implicitly_wait(2)
    time.sleep(.1)
    matches = driver.find_elements(By.XPATH, '//div[@data-cy="teamMatchHistoryOpponent"]//*[img]')
    for match in matches:
        # Opens and Switches to Match
        match.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        # Scrape Player Data
        driver.implicitly_wait(10)
        completed = driver.find_elements(By.XPATH, '//p[contains(text(), "Completed")]')
        if completed:
            driver.implicitly_wait(5)
            scraped_team = driver.find_element(By.XPATH, f'//a[contains(text(), "{team.name}")]')
            # since page first loads in the wrong orientation, this waits out until it is correct
            start = time.time()
            while time.time() - start < 1:
                last_team = scraped_team
                driver.implicitly_wait(5)
                scraped_team = driver.find_element(By.XPATH, f'//a[contains(text(), "{team.name}")]')
                if last_team != scraped_team:
                    start = time.time()
            driver.implicitly_wait(5)
            scraped_team = driver.find_element(By.XPATH, f'//a[contains(text(), "{team.name}")]')
            if len(driver.find_elements(By.XPATH, '//p[contains(text(), "Game")]')) > 0:
                alignment = scraped_team.value_of_css_property('text-align')
                home = alignment == 'left'
                driver.implicitly_wait(5)
                xpath = '//div[div[div[div[div[div[p[contains(text(), "Series")]]]]]]]'
                series = driver.find_elements(By.XPATH, xpath)
                for number in range(len(series)):
                    ser = series[number]
                    name = unidecode(ser.find_elements(By.XPATH, './/p[..[..[p]]]')[0 if home else 1].text)
                    game_stages = ser.find_elements(By.XPATH, './/p[..[p[contains(text(), "Game")]]]')
                    stages = [unidecode(game_stages[x * 2 + 1].text) for x in range(int(len(game_stages) / 2))]
                    triangles = ser.find_elements(By.CSS_SELECTOR, 'div[data-cy="leftTriangle"]')[1:]
                    results = [(x.value_of_css_property('visibility') == 'visible') == home for x in triangles]
                    player_chars = []
                    opponent_chars = []
                    series_games = ser.find_elements(By.XPATH, './/div[div[div[p[contains(text(),"Game")]]]]')
                    for series_game in series_games:
                        time.sleep(.02)
                        circles = series_game.find_elements(By.XPATH, './/div/div/div/div[p]')
                        i = 0
                        for circle in circles:
                            letter = circle.find_element(By.TAG_NAME, "p").text
                            character = ''
                            start = time.time()
                            while character == '' and time.time() - start < 1:
                                driver.implicitly_wait(5)
                                actions.move_to_element(circle).perform()
                                driver.implicitly_wait(5)
                                driver.execute_script(f'window.scrollTo(0, {circle.location["y"]})')
                                driver.implicitly_wait(5)
                                actions.move_to_element(circle).perform()
                                time.sleep(.05)
                                driver.implicitly_wait(5)
                                xpath = f'//div/div[contains(text(), "{letter}")][not(contains(text(),"cookies"))]'
                                if len(driver.find_elements(By.XPATH, xpath)) > 0:
                                    div = driver.find_element(By.XPATH, xpath)
                                    character = unidecode(div.text)
                                    if character == '':
                                        character = div.get_attribute("innerHTML")
                                    print(f'{i} ({letter}) {character}')
                            if home == (i % 2 == 0):
                                player_chars.append(character)
                            else:
                                opponent_chars.append(character)
                            i += 1
                    team.add_series(name, number + 1, list(zip(player_chars, opponent_chars, stages, results)))
        # Close Match and Return to Team
        driver.close()
        driver.switch_to.window(windows[0])
    return team
