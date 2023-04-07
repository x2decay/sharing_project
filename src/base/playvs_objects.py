from selenium.webdriver.common.by import By

headers = ['Character', 'Opponent', 'Stage', 'Result']


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
        self.series_list = []

    def add_series(self, number, games):
        self.series_list.append(Series(number, games))

    def games(self):
        games = []
        for s in self.series_list:
            games += s.games
        return games

    def key(self, k):
        return [d[k] for d in self.games()]

    def print_stats(self):
        results = self.key('Result')
        print(f'Win Percent: {round(results.count(True) / len(results) * 100, 1)}%')
        played = [s.number for s in self.series_list]
        for n in range(3):
            print(end=f'{["First", "Second", "Third"][n]}: {played.count(n + 1)} ')
        results = list(reversed(self.key('Result')))
        if results.count(True) > 0:
            last_won = list(reversed(self.games()))[list(reversed(results)).index(True)]
            print(end=f'\nLast win was as {last_won["Character"]} ')
            print(f'against {last_won["Opponent"]} on {last_won["Stage"]}')
        else:
            print('\nNo won games on record')
        for header in headers:
            print(f'\t{header} Win Percents')
            self.win_percent(header)

    def print_games(self):
        for game in self.games():
            print(end=f'{"Won" if game["Result"] else "Lost"} as ')
            print(f'{game["Character"]} against {game["Opponent"]} on {game["Stage"]}')

    def win_percent(self, mode):
        var = self.key(mode)
        results = self.key('Result')
        won = {}
        total = {}
        for i in range(len(results)):
            if var[i] not in won:
                won[var[i]] = 0
                total[var[i]] = 0
            if results[i]:
                won[var[i]] += 1
            total[var[i]] += 1
        percent = {char: round(won[char] / total[char] * 100, 1) for char in var}
        for char in percent:
            print(f'\t\t{char}:\t{percent[char]}% ({total[char]} game{"s" if total[char] > 1 else ""})')


class Series(object):
    def __init__(self, number, games):
        self.number = number
        self.games = [{h: x for (h, x) in zip(headers, g)} for g in games]
