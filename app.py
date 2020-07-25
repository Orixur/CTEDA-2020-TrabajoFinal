import os

from flask import Flask, render_template, request, jsonify

from main import load_game_config

app = Flask(__name__)

yaml_location = os.environ['GAME_CONFIG']
game_config = load_game_config(yaml_location)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/p1', methods=['GET', 'POST'])
def p1():
    player = 'p1'
    return render_template('players.html', file_data='', player=player)

@app.route('/p2', methods=['GET', 'POST'])
def p2():
    player = 'p2'
    return render_template('players.html', file_data='', player=player)

@app.route('/get_data_p1')
def get_data_p1():
    my_player = 'p1'
    response = {}
    with open(game_config['players_info'][my_player]['dump_location'], 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace('\n', '<br>')
        data = data.replace('\t', '&nbsp;' * 12)
        response['data'] = data
    
    return jsonify(response)

@app.route('/get_data_p2')
def get_data_p2():
    my_player = 'p2'
    response = {}
    with open(game_config['players_info'][my_player]['dump_location'], 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')
        data = data.replace('\n', '<br>')
        data = data.replace('\t', '&nbsp;' * 12)
        response['data'] = data
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
