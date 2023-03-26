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
    headers = ['Characters', 'Opponents', 'Stages', 'Results', 'Series_Order', 'Game_Order']

    def __init__(self, name):
        self.name = name
        self.games_list = []

    def games(self):
        return [{self.headers[i][:-1]: g[i] for i in range(len(g))} for g in self.games_list]

    def zipped(self):
        return {header: data for (header, data) in zip(Player.headers, zip(*self.games_list))}

    def stats(self):
        print(list(filter(lambda x: x > 0, self.zipped()['Series_Order'])))
        for header in Player.headers[:3]:
            print(f'\t{header[:-1]} Win Percents')
            self.win_percent(header)

    def print_games(self):
        for game in self.games():
            print(f'{"Won" if game["Result"] else "Lost"} as ', end='')
            print(f'{game["Character"]} against {game["Opponent"]} on {game["Stage"]}')

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
            print(f'\t\t{char}:\t{percent[char]}% ({total[char]} game{"s" if total[char] > 1 else ""})')
