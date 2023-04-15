from selenium.webdriver.common.by import By

HEADERS = ['Character', 'Opponent', 'Stage', 'Result']


class Team(object):
    def __init__(self, data, from_json=False):
        if from_json:
            self.school = data['school']
            self.href = data['href']
        else:
            self.school = self.__get_school(data)
            self.href = self.__get_href(data)
        self.players = {}

    def add_series(self, name, number, games):
        if name not in self.players:
            self.players[name] = Player()
        self.players[name].add_series(number, games)

    @staticmethod
    def __get_school(data):
        return data.find_elements(By.XPATH, 'div//a/p[text()]')[1].text

    @staticmethod
    def __get_href(data):
        return data.find_element(By.XPATH, 'div//a').get_attribute('href')


class Player(object):
    def __init__(self):
        self.series = []

    def add_series(self, number, games):
        self.series.append(Series(number, games))

    def games(self):
        games = []
        for s in self.series:
            games += s.games
        return games

    def key(self, key):
        return [game[key] for game in self.games()]

    def print_stats(self):
        results = self.key('Result')
        print(f'Win Percent: {round(results.count(True) / len(results) * 100, 1)}%')
        played = [s.number for s in self.series]
        for n in range(3):
            print(end=f'{["First", "Second", "Third"][n]}: {played.count(n + 1)} ')
        results = list(reversed(self.key('Result')))
        if results.count(True) > 0:
            last_won = list(reversed(self.games()))[list(reversed(results)).index(True)]
            print(end=f'\nLast win was as {last_won["Character"]} ')
            print(f'against {last_won["Opponent"]} on {last_won["Stage"]}')
        else:
            print('\nNo won games on record')
        for header in HEADERS[:-1]:
            print(f'\t{header} Win Percents')
            self.win_percent(header)

    def print_games(self):
        for game in self.games():
            print(end=f'{"Won" if game.result else "Lost"} as ')
            print(f'{game.character} against {game.opponent} on {game.stage}')

    def win_percent(self, mode):
        keys = self.key(mode)
        results = self.key('Result')
        items = {}
        for i in range(len(results)):
            if keys[i] not in items:
                items[keys[i]] = [keys[i], 0, 0]
            if results[i]:
                items[keys[i]][1] += 1
            items[keys[i]][2] += 1
        for (key, won, total) in sorted(items.values(), key=lambda x: x[2], reverse=True):
            print(f'\t\t{key + ":":<21}{round(won / total * 100):>3}% won over {total} game{"s" if total > 1 else ""}')


class Series(object):
    def __init__(self, number, games):
        self.number = number
        self.games = [Game(*g) for g in games]


class Game(object):
    def __init__(self, character, opponent, stage, result):
        self.character = character
        self.opponent = opponent
        self.stage = stage
        self.result = result
        self.__index = 0

    def __iter__(self):
        return [self.character, self.opponent, self.stage, self.result]

    def __getitem__(self, key):
        if type(key) == str:
            key = HEADERS.index(key)
        return self[key]

    def __next__(self):
        if self.__index > len(HEADERS):
            self.__index = 0
            raise StopIteration
        else:
            self.__index += 1
            return self[self.__index]
