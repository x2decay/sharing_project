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

    def add_player(self, name):
        self.players[name] = Player(name)

    def add_game(self, name, game):
        self.players[name].add_game(game)


class Player(object):
    def __init__(self, name):
        self.name = name
        # [Character, Opponent, Stage, win/lose]
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def characters(self):
        chars = list(zip(*self.games))[0]
        for char in sorted(set(chars)):
            print(f'{char}:\t{chars.count(char)/len(chars)}')
