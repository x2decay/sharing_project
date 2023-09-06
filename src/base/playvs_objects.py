from selenium.webdriver.common.by import By

HEADERS = ['Character', 'Opponent', 'Stage', 'Result']


class Team(object):
    def __init__(self, data, from_json=False):
        if from_json:
            self.name = data['name']
            self.school = data['school']
            self.href = data['href']
        else:
            self.name = Team.__get_name(data)
            self.school = Team.__get_school(data)
            self.href = Team.__get_href(data)
        self.players = []

    def add_series(self, name, number, games):
        if name not in self.names():
            self.players.append(Player(name))
        self.players[self.names().index(name)].add_series(number, games)
        self.players.sort(key=lambda x: max([1, 2, 3], key=[s.number for s in x.series].count))

    def names(self):
        return [p.name for p in self.players]

    @staticmethod
    def __get_name(data):
        return data.find_elements(By.XPATH, './/p[text()]')[0].text

    @staticmethod
    def __get_school(data):
        return data.find_elements(By.XPATH, './/p[text()]')[1].text

    @staticmethod
    def __get_href(data):
        return data.find_element(By.TAG_NAME, 'a').get_attribute('href')


class Player(object):
    def __init__(self, name):
        self.name = name
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
        print(f'Win Percent: {round(results.count(True) / len(results) * 100)}%')
        played = [s.number for s in self.series]
        for n in range(3):
            print(end=f'{["First", "Second", "Third"][n]}: {played.count(n + 1)} ')
        if results.count(True) > 0:
            last_won = list(reversed(self.games()))[list(reversed(results)).index(True)]
            print(end=f'\nLast win was as {last_won["Character"]} ')
            print(f'against {last_won["Opponent"]} on {last_won["Stage"]}')
        else:
            print('\nNo won games on record')
        for header in HEADERS[:-1]:
            print(f'\t{header} Win Percentages:')
            self.print_win_percent(header)

    def line_stats(self):
        lines = []
        results = self.key('Result')
        lines.append(f'<p style="font-family: Consolas">Win Percent: '
                     f'{round(results.count(True) / len(results) * 100)}%<br>')
        played = [s.number for s in self.series]
        for n in range(3):
            lines.append(f'{["First", "Second", "Third"][n]}: {played.count(n + 1)} ')
        if results.count(True) > 0:
            last_won = list(reversed(self.games()))[list(reversed(results)).index(True)]
            lines.append(f'<br>Last win was as {last_won["Character"]} ')
            lines.append(f'against {last_won["Opponent"]} on {last_won["Stage"]}</p>')
        else:
            lines.append('<br>No won games on record</p>')
        for header in HEADERS[:-1]:
            lines.append(f'<br><h4 style="font-family: Consolas">{header} Win Percentages:</h4>'
                         f'<p style="font-family: Consolas">')
            lines += self.line_win_percent(header)
        return lines

    def print_games(self):
        for game in self.games():
            print(end=f'{"Won" if game.result else "Lost"} as ')
            print(f'{game.character} against {game.opponent} on {game.stage}')

    def print_win_percent(self, mode):
        keys = self.key(mode)
        results = self.key('Result')
        items = {}
        for i in range(len(results)):
            if keys[i] not in items:
                items[keys[i]] = [keys[i], 0, 0]
            if results[i]:
                items[keys[i]][1] += 1
            items[keys[i]][2] += 1
        for (k, w, t) in sorted(items.values(), key=lambda x: x[2], reverse=True):
            print(f'\t\t{k + ":":<21} {round(w / t * 100):>3}% won over {t} game{"s" if t > 1 else ""}')

    def line_win_percent(self, mode):
        keys = self.key(mode)
        results = self.key('Result')
        items = {}
        for i in range(len(results)):
            if keys[i] not in items:
                items[keys[i]] = [keys[i], 0, 0]
            if results[i]:
                items[keys[i]][1] += 1
            items[keys[i]][2] += 1
        lines = []
        for (k, w, t) in sorted(items.values(), key=lambda x: x[2], reverse=True):
            p = str(round(w / t * 100))
            lines.append(f'{k}:{"&nbsp"*(24-len(k+p))}{p}% won over {t} game{"s" if t > 1 else ""}<br>')
        return lines + ['</p>']


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

    def __iter__(self):
        self.__index = 0
        return self

    def list(self):
        return [self.character, self.opponent, self.stage, self.result]

    def __getitem__(self, key):
        if type(key) == str:
            key = HEADERS.index(key)
        return self.list()[key]

    def __next__(self):
        if self.__index > len(HEADERS):
            self.__index = 0
            raise StopIteration
        else:
            self.__index += 1
            return self[self.__index]
