import os
import sys
import yaml

from game.game_controller import Game
from game.node import Node
from game.cpu_controller import CPUBrain
from game.human_controller import HumanController

def load_game_config(path: str) -> dict:
    with open(path, 'r') as f_buffer:
        try:
            aux = yaml.safe_load(f_buffer)
            return aux['game_config']
        except yaml.YAMLError as exc:
            raise exc

def generate_player_mapping(players_info: dict, limit: int) -> dict:
    aux = {}
    cpu_players = []

    for player, player_info in players_info.items():
        aux[player] = {}
        if player_info['type'] == 'human':
            aux[player]['instance'] = HumanController(who_am_i=player, alias=player_info['alias'])
        elif player_info['type'] == 'cpu':
            cpu_players.append(player)
            aux[player]['instance'] = CPUBrain(who_am_i=player, main_root=Node(None, limit, 0, how_moves=None), alias=player_info['alias'], dump_dir=player_info['dump_location'])

    return aux, cpu_players

if __name__ == '__main__':
    # Cargar YAML
    yaml_location = os.environ['GAME_CONFIG']
    game_config = load_game_config(yaml_location)

    # Levantar las instancias de los controladores
    player_mapping, cpu_players = generate_player_mapping(game_config['players_info'], limit=game_config['limit'])

    # Inicializar una instancia de Game
    game = Game(game_config['limit'], players_name_mapping=player_mapping, cpu_players=cpu_players,\
                q_cards=game_config['deck_size'], lower_threshold_limit=game_config['lower_threshold_limit'], higher_threshold_limit=game_config['higher_threshold_limit'])

    # Iniciar el juego
    game.start()
