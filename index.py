from flask import Flask
import src.base.json_conversion as json

app = Flask('__main__')


@app.route('/')
def home():
    with open('archived_teams.json', 'r') as file:
        team = json.to_object(file)
    return ''.join(['<h2 style="font-family: Consolas">' + p.name +
                    '</h2>' + ''.join(p.line_stats()) + '<br>'
                    for p in team.players])


if __name__ == '__main__':
    app.run()
