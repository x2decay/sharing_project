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
    headers = ['Characters', 'Opponents', 'Stages', 'Results']

    def __init__(self, name):
        self.name = name
        self.games = []

    def zipped(self):
        return {header: data for (header, data) in zip(Player.headers, zip(*self.games))}

    def stats(self):
        for header in Player.headers[:-1]:
            print(f'  {header[:-1]} Win Percents')
            self.win_percent(header)

    def characters(self):
        self.win_percent('Characters')

    def opponents(self):
        self.win_percent('Opponents')

    def stages(self):
        self.win_percent('Stages')

    def win_percent(self, mode):
        var = self.zipped()[mode]
        results = self.zipped()['Results']
        won = {}
        total = {}
        for i in range(len(results)):
            if var[i] not in won:
                won[var[i]] = 0
                total[var[i]] = 0
            if results[i]:
                won[var[i]] += 1
            total[var[i]] += 1
        percent = {char: round(won[char]/total[char]*100, 1) for char in var}
        for char in percent:
            print(f'    {char}:\t{percent[char]}% ({total[char]} game{"s" if total[char] > 1 else ""})')
