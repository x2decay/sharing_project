from selenium.webdriver.common.by import By


class Team(object):
    def __init__(self, raw_data):
        self.name = self.__get_name(raw_data)
        self.school = self.__get_school(raw_data)
        self.href = self.__get_href(raw_data)
        self.players = {}

    @staticmethod
    def __get_name(raw_data):
        return raw_data.find_elements(By.XPATH, 'div//a/p[text()]')[0].text

    @staticmethod
    def __get_school(raw_data):
        return raw_data.find_elements(By.XPATH, 'div//a/p[text()]')[1].text

    @staticmethod
    def __get_href(raw_data):
        return raw_data.find_element(By.XPATH, 'div//a').get_attribute('href')

    def add_game(self, name, game):
        self.players[name].add_game(game)


class Player(object):
    def __init__(self, name, games):
        self.name = name
        self.headers = ['Characters', 'Opponents', 'Stages', 'Results']
        self.games = games
        self.zipped = {header: data for (header, data) in zip(self.headers, zip(*games))}

    def characters(self):
        characters = self.zipped['Characters']
        results = self.zipped['Results']
        won = {}
        total = {}
        for i in range(len(results)):
            if characters[i] not in won:
                won[characters[i]] = 0
                total[characters[i]] = 0
            if results[i]:
                won[characters[i]] += 1
            total[characters[i]] += 1
        percent = {char: round(won[char]/total[char], 3)*100 for char in characters}
        for char in percent:
            print(f'{char}:\t{percent[char]}%')
