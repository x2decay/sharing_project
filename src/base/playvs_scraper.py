from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
import time
from playvs_objects import *

# Initialization
url = 'https://app.playvs.com/app/standings'
email = 'lkryvenko@cherrycreekschools.org'
password = 'Dogunderfifthdollartree.'
driver = webdriver.Firefox(os.path.abspath('geckodriver'))
wait = WebDriverWait(driver, 2)
actions = ActionChains(driver)
driver.get(url)

# Login
driver.implicitly_wait(2)
email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
email_input.send_keys(*list(email))
password_input.send_keys(*list(password))
password_input.send_keys(Keys.ENTER)

# Switch to Dark Mode (Better for your Eyes!)
driver.implicitly_wait(5)
settings = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="account-settings-navigation"]')
settings.click()
driver.implicitly_wait(2)
dark = driver.find_elements(By.CSS_SELECTOR, 'li[role="menuitem"]')[6]
dark.click()
dark.send_keys(Keys.ESCAPE)

# Switch to Smash
driver.implicitly_wait(2)
league = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Colorado CHSAA League of Legends"]')
driver.execute_script("arguments[0].click();", league)
driver.implicitly_wait(2)
smash = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Colorado CHSAA Super Smash Bros.™ Ultimate"]')
smash.click()

# Switch to Spring 2023
driver.implicitly_wait(5)
season = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Fall 2022"]')
season.click()
driver.implicitly_wait(2)
spring23 = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Spring 2023"]')
spring23.click()

# Switch to Regular Season
driver.implicitly_wait(5)
season = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="Playoffs"]')
season.click()
driver.implicitly_wait(2)
spring23 = driver.find_element(By.CSS_SELECTOR, 'li[data-cy="Regular Season"]')
spring23.click()

# Scrape the Teams
driver.implicitly_wait(2)
body = driver.find_element(By.XPATH, '//div[..[p[text()[contains(.,"Overall")]]]]')
teams = {x.name: x for x in
         [Team(x) for x in body.find_elements(By.CSS_SELECTOR, 'div[role="row"]')[7:8]]}  # n for opt

# Loop through the Teams, also accepts input on which Team to Select
loop = True
i = 0
name = '' if True else input('Enter team name: ')
while loop:
    team = teams[name if name != '' else list(teams.keys())[i]]
    # Opens Team Page
    driver.get(team.href)
    # Ensures All Matches are Selected
    driver.implicitly_wait(5)
    print(driver.find_element(By.XPATH, f'//p[contains(text(),"{team.name}")]').text)
    more = driver.find_elements(By.XPATH, '//span/div[contains(text(),"Show More")]')
    if len(more) > 0:
        more[0].click()
    # Goes through Every Match
    driver.implicitly_wait(2)
    matches = driver.find_elements(By.XPATH, '//div[@data-cy="teamMatchHistoryOpponent"]//*[img]')
    for match in matches:
        print(matches.index(match))
        # Opens and Switches to Match
        match.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        # Scrape Player Data
        xpath = '/html/body/div[1]/div/div/div[2]/div[2]/div/div[1]'
        driver.implicitly_wait(5)
        banner = driver.find_element(By.XPATH, xpath)
        a = banner.find_elements(By.TAG_NAME, 'a')
        home = a[2].text == team.name
        xpath = '/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[2]/div'
        time.sleep(2)
        p = driver.find_element(By.XPATH, xpath).find_elements(By.TAG_NAME, 'p')
        scores = [[int(x[0]), int(x[-1])] for x in filter(lambda x: ' - ' in x, [x.text for x in p])]
        stages = []
        for i in range(len(p) - 1):
            if 'GAME' in p[i].text:
                stages.append(p[i + 1].text)
        names = []
        for i in range(len(p) - 1):
            if home and 'SERIES' in p[i].text or not home and ' - ' in p[i].text:
                names.append(p[i + 1].text)
        left_triangles = driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="leftTriangle"]')
        # for x in range(len(p)):
        #     print(f'{x}:\t{p[x].text}')
        home_score = driver.find_element(By.CSS_SELECTOR, 'p[data-cy="teamScore"]')
        away_score = driver.find_element(By.CSS_SELECTOR, 'p[data-cy="opponentScore"]')
        for series in range(int(home_score.text) + int(away_score.text)):
            team.add_player(names[series])
            # TODO:
            #  - Win? (arrow direction)
            #  - Hover to see character name (trigger hover, then peek)
            # https://stackoverflow.com/questions/74342917/extract-text-on-mouse-hover-in-python-selenium
            # desired_elem = wait.until(
            #     EC.visibility_of_element_located((By.CSS_SELECTOR, '.SdgPerformanceBar__Block-sc-1yl1q71-2.fBQLcJ')))
            # actions.move_to_element(desired_elem).perform()
            # tt1_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tooltip1))).text
            for game in range(sum(scores[series])):
                print(stages[0])
                jss = driver.find_element(By.CSS_SELECTOR, '[data-cy="leftTriangle"]').get_attribute("class").split()[1]
                soup = BeautifulSoup(requests.get(driver.current_url).text, 'lxml')
                element = soup.find(class_=jss)
                if element is not None:
                    visible = element.get('style', '').split(':')[-1].strip()
                else:
                    visible = 'hidden'
                print(visible)
                game_won = visible == home
                print(visible, home)
                print('Won!' if game_won else 'Lost ;(')
                team.add_game(names[series], ['Character', 'Opponent', stages.pop(0), game_won])
            print()
        input('->')
        # Close Match and Return to Team
        driver.close()
        driver.switch_to.window(windows[0])
    # Does cycle, also allows program to exit
    name = '' if True else input('Enter team name\n> ')
    i += 0 if name != '' else 1
    if name == 'quit' or i >= len(teams):
        loop = False

input('quit?')
print('quiting...', end='')
driver.quit()
