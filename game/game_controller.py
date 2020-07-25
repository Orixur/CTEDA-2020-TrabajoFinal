import copy
import random

from game import exceptions
from game.cpu_controller import CPUBrain


class Game:
    """
        Esta clase engloba todas las funcionalidaes base para el funcionamiento de una partida.\n
        
        Attributes:
            maximum_mount_limit (int): limite máximo permitido para el monto de descarte
            players_name_mapping (dict): Diccionario que contendrá las 2 ids de jugadores
                como clave y la instancia de sus controladores como valor
            q_cards (int): Cantidad de cartas para el juego actual
            cpu_players (tuple): tupla que contiene los ids de jugadores que serán CPUPlayers
            lower_threshold_limit (int): Porcentaje mínimo para la selección del limite del monto
            higher_threshold_limit (int): Porcentaje máximo para la selección del limite del monto
    """
    def __init__(self, limit: int, players_name_mapping: dict, q_cards: int, cpu_players: tuple, lower_threshold_limit: int, higher_threshold_limit: int):
        self.maximum_mount_limit = limit
        self.players_name_mapping = players_name_mapping
        self.q_cards = q_cards
        self.cpu_players = cpu_players

        self.lower_threshold_limit = lower_threshold_limit
        self.higher_threshold_limit = higher_threshold_limit

    def decide_first_player(self) -> list:
        """
            Esta función mezcla aleatoriamente los 2 ids de jugadores,
            y devuelve ese resultado. El mismo representará el
            orden de los jugadores.\n
            El orden de los jugadores no es un valor trivial para una partida.

            Returns:
                list: Ids de jugadores en orden
        """
        players = list(self.players_name_mapping.keys())
        random.shuffle(players)

        return players

    def validate_limit(self) -> bool:
        """
            Esta función se encarga de validar el límite impuesto, basado
            en la cantidad de cartas que tendrá el mazo (ambas variables de instancia).\n
            Esta evaluación se hace obteniendo el valor porcentual relativo del limite
            para con el máximo de cartas del mazo.\n
            Si el mismo no se encuentra comprendido entre los limites de la instancia,
            se devolverá un valor False, derivando en una excepción terminante.

            Returns:
                bool: Resultado de la evaluación del limite
        """
        max_sum = sum(range(1, self.q_cards+1))
        porcentual_limit = ((self.maximum_mount_limit) * (100)) / (max_sum)

        if self.lower_threshold_limit <= porcentual_limit <= self.higher_threshold_limit:
            return True, porcentual_limit
        return False, porcentual_limit

    def create_deck(self) -> list:
        """
            Esta función crea el mazo a utilizar y lo mezcla de forma aleatoria.\n
            El naming para los valores a crear es un rango entre: 1 y la cantidad máxima de cartas.

            Returns:
                list: Lista de valores aleatorios (Mazo)
        """
        cards_naming_range = range(1, self.q_cards+1)
        deck = list(cards_naming_range)
        random.shuffle(deck)

        return deck

    def start(self):
        """
            Rutina de juego.\n
            La misma se encargá de guardar una copia profunda (no Shallow)
            de las instancias de los jugadores (previo a que, por ejemplo,
            un jugador CPU calcule los movimientos de la partida).\n
            El orden de esta rutina será:\n
            \t1. En principio se valida el limite pasado como parámetro, derivando
            en una excepción terminante si el mismo no es valido.\n
            \t2. Luego se identifican las instancias del primer y segundo jugador y
            se les asignan sus respectivas manos\n
            \t3. Posteriormente se verifica que jugador es CPU y en ese caso, se le pide
            que simule todos los movimientos posibles (esta sección no aplica a controladores de humanos)\n
            \t4. Se abre el bucle de juego, el mismo seguirá iterando sobre varios turnos hasta que un jugador pierda.\n
            Cabe hacer las siguientes aclaraciones:\n
            \t- Es indistinto para el juego si hay 1 jugador humano y uno maquina, o si son 2 humanos o 2 maquinas
            las interfaces de juego de ambos controladores son análogas.\n
            \t- Al comienzo y al final de cada iteración (turno) se correrá una porción de código que se encargá
            de hacer el dump de cada jugador CPU a su archivo correspondiente.\n
            \t- Luego de que se corté el bucle de juego, y haya al menos 1 jugador humano se le
            preguntará si quiere volver a jugar (esta funcionalidad no tiene que reiniciar los estados de los controladores
            de jugadores, puesto que al comienzo de esta función se hace una copia profunda de los mismos)\n
        """
        current_game_players = copy.deepcopy(self.players_name_mapping)
        limit_validation = self.validate_limit()
        if limit_validation[0]:
            print(f'Limite valido! (Limite porcentual relativo al máximo monto de descarte: {limit_validation[1]}%)')
        else:
            print(f'Limite no valido! (Limite porcentual relativo al máximo monto de descarte: {limit_validation[1]}%)')
            raise exceptions.WrongGameConfigurationError(f'Ha provisto un limite que no se encuentra entre los limites: {self.lower_threshold_limit} < x < {self.higher_threshold_limit}')

        player_order = self.decide_first_player()
        first_player = current_game_players[player_order[0]]['instance']
        second_player = current_game_players[player_order[1]]['instance']

        deck = self.create_deck()
        first_player.my_cards = deck[:int((len(deck)/2))]
        second_player.my_cards = deck[int((len(deck)/2)):]

        # Detecto cuales jugadores son cpu y en ese caso hago generen su cerebro
        if isinstance(first_player, CPUBrain):
            first_player.simulate_moves(first_player.main_root, first_player.my_cards, second_player.my_cards, 0, first_player.who_am_i, self.maximum_mount_limit)
        
        if isinstance(second_player, CPUBrain):
            second_player.simulate_moves(second_player.main_root, first_player.my_cards, second_player.my_cards, 0, first_player.who_am_i, self.maximum_mount_limit)

        global_mount_count = 0
        last_card = None
        turno = 0
        while True:  # Mientras el monto total siga sin pasar el limite, se continua el juego
            for cpu_player in self.cpu_players:
                current_game_players[cpu_player]['instance'].dump_brain()
            print('\n--------------------------------------------------------------------------------')
            print('Comenzando un nuevo turno...')
            print(f'Actualmente nos encontramos en el turno: {turno}')
            print(f'El monto actual es de {global_mount_count} (el limite es de {self.maximum_mount_limit})')

            print('\n')

            print(f'Y le toca jugar a {first_player.alias}!')
            first_player_move = first_player.play_a_move(last_card)
            print(f'El jugador {first_player.alias} ha descartado la carta: {first_player_move}')
            last_card = first_player_move
            global_mount_count += first_player_move
            if global_mount_count > self.maximum_mount_limit:
                print(f'\nEl jugador {first_player.who_am_i} pierde! Sobrepaso el limite del juego ({global_mount_count})')
                print(f'Felicidades {second_player.alias} has vencido!')
                break

            print('\n')
            print(f'\nEl monto se ha aumentado a {global_mount_count}!!')

            print(f'Esperando el movimiento de  {second_player.alias}!')
            second_player_move = second_player.play_a_move(last_card)
            print(f'El jugador {second_player.alias} ha descartado la carta: {second_player_move}')
            last_card = second_player_move
            global_mount_count += second_player_move
            if global_mount_count > self.maximum_mount_limit:
              print(f'\nEl jugador {second_player.who_am_i} pierde! Sobrepaso el limite del juego ({global_mount_count})')
              print(f'Felicidades {first_player.alias} has vencido!')
              break

            for cpu_player in self.cpu_players:
                current_game_players[cpu_player]['instance'].dump_brain()
            turno += 1
        
        if len(self.cpu_players) == 2:
            pass
        else:
            res = input('Quiere volver a jugar una nueva partida? [y/n]: ')
            if res == 'y' or res == 'Y':
                self.start()
