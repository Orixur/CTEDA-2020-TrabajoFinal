import random
import copy

from game.node import Node

class CPUBrain:
    """
        Esta clase fue diseñada para que implemente las funcionalidades
        necesarias para que un jugador CPU sea capaz de interactura con otro
        jugador por medio de una rutina de juego.\n
        Esta clase tiene como carácteristica principal la creación de un mapeo
        de todos los posibles movimientos que se pueden dar para un número
        N de cartas, y otros factores que determinan los estados y al juego.\n
        Esta clase puede ser puesta a jugar contra un controlador humano, o
        contra otro controlador CPU.\n
        Adicionalmente, esta clase soporta la asignación de cualquier de los 2
        posibles ids de jugador que soporta el sistema. Esto se traduce en que, el calculo
        de jugadas no se encuentra hardcodeado para un jugador en concreto, y a la vez
        habilita la adición de otro jugador CPU al juego.

        Attributes:
            who_am_i (str): Id del jugador
            VALUES (dict): Consiste en un diccionario el cual
                tendrá los valores heuristicos basados en este jugador
            main_root (Node): Este nodo es el nodo base del que se crean las predicciones
                sobre un juego
            my_cards (list): Lista de valores/cartas que se le disponibilizaron
            __all_nodes (list): Lista que contiene todos los nodos cargados para
                un juego en concreto
            alias (str): Nombre alternativo utilizado durante el juego para referirse
                a este personaje
            current_game_root (Node): Este nodo comienza siendo el nodo `main_root`,
                la diferencia entre ambos es que este irá alternando su valor,
                a lo largo del juego, pasando a ser la raiz de distintos instantes
                de una partida
            dump_dir (str): Ruta completa al archivo de dumpeo para trackear el
                cerebro de este jugador en tiempo real
    """
    def __init__(self, who_am_i: str, main_root: Node, alias: str, dump_dir: str):
        self.who_am_i = who_am_i  # Jugador que queremos maximizar (A.K.A Cpu player)
        self.load_heuristic_mapping()
        self.main_root = main_root
        self.my_cards = []
        self.__all_nodes = [self.main_root]
        self.alias = alias
        self.current_game_root = self.main_root  # Esta es la raiz que se va a ir actualizando durante el transcurso del juego
        self.dump_dir = dump_dir

    def play_a_move(self, last_card: int) -> int:
        """
            Esta función es la análoga a al función `game.human_controller.HumanController.play_a_move`.\n
            En este caso los pasos que sigue esta función son:\n
            \t1. Fijarse si el parámetor last_card recibido actualmente es None. En tal caso estamos
            ante el primer instante de una partida, y por ende este jugador es el primero en mover.\n
            \t2. Si la ultima carta es distinta a None, entonces estamos en un turno mas avanzado que el primero.\n
            \t\tEsto significa que se deberá mover la variable de instancia `self.current_game_root` al
            nodo que coresponda. Para esto buscamos entre los hijos del estádo actual, cual de ellos contiene
            el valor de la ultima carta recibida.\n
            \t\tPosteriormente se procede a buscar el mejor hijo posible, esto se hace utilizando la función
            `self.search_best_child_based_on_win_rate()`. Tal y como el nombre lo explica, se buscará el mejor
            hijo comparando los valores de ratio de victoria (win_rate).\n
            \t\tUna vez encontrado el mejor hijo, se actualiza el estado de `self.current_game_root` a que sea
            el mejor hijo encontrado, se elimina la opción elegida de nuestra lista de cartas y se devuelve
            la elección tomadá.\n

            Args:
                last_card (int): Ultima carta jugada por el jugador adversario, servirá para actualizar
                    el estado actual de la partida y tomar una decisión en base a ello

            Returns:
                choice (int): Devuelve la elección tomada (devolverá el atributo `Node.data` del mejor_hijo,
                    representando la mejor carta posible a jugar)
        """
        print(f'{self.alias} - Cards: {self.my_cards}')
        if last_card is None:  # Osea, si este jugador es el primero en mover
            # En este caso no tenemos que actualizar la raiz de seguimiento del juego al movimiento anterior del rival
            # puesto que somos los primeros en mover
            best_child = self.search_best_child_based_on_win_rate()  # Busco el hijo que maximice mis oportunidades de ganar
        
            self.current_game_root = best_child  # Muevo el estado del juego al mejor hijo encontrado
        else:
            for child in self.current_game_root.childs:  # Para cada hijo de la raiz del juego actual...
                if child.data == last_card:  # Me fijo cual es el nodo que le corresponde al ultimo movimiento del rival, en base a los hijos actuales
                    self.current_game_root = child  # Seteo al estado actual, como la opción que tomo el rival en su ultimo turno
                    break

            best_child = self.search_best_child_based_on_win_rate()  # Busco el hijo que maximice mis oportunidades de ganar
            
            self.current_game_root = best_child  # Muevo el estado del juego al mejor hijo encontrado
        
        del self.my_cards[self.my_cards.index(best_child.data)]
        print(f'La mejor jugada es elegir <{best_child.data}>, tengo un win rate de {best_child.win_rate}% (W-L: {best_child.wins}-{best_child.loses})')
        return best_child.data  # Retorno la carta que hubiera jugado la cpu

    def search_best_child_based_on_win_rate(self) -> Node:
        """
            Esta función devuelve el mejor hijo basado en un momento en concreto
            de la partida actual.\n
            El mejor hijo se encontrará en base al atributo `Node.win_rate` de cada hijo.

            Returns:
                Node: Mejor hijo
        """
        best_win_rate = float('-inf')
        best_child = None
        for child in self.current_game_root.childs:  # Para cada hijo de la raiz del juego actual...
            if child.win_rate > best_win_rate:  # Me fijo que hijo me da mas posibilidades de ganar
                best_win_rate = child.win_rate
                best_child = child

        return best_child

    def load_heuristic_mapping(self):
        """
            Carga el mapeo de valores estáticos heuristicos.\n
            Este mapeo se hace en base al id del jugador actual,
            puesto que el sistema admite solo 2 jugadores los 2 posibles
            ids a asignar a un jugador humano/cpu son:\n
            \t- p1\n
            \t- p2\n
            Los valores heuristicos aca generados serán utilizados durante
            la simulación de todos los posibles escenarios (cerebro del jugador CPU).
        """
        self.VALUES = {}
        if self.who_am_i is 'p1':
            self.VALUES['p1'] = 1
            self.VALUES['p2'] = -1
        else:
            self.VALUES['p1'] = -1
            self.VALUES['p2'] = 1
        self.VALUES['n/a'] = 0

    def simulate_moves(self, root: Node, current_moves: list, next_moves: list, depth: int, how_moves: str, limit: int):
        """
            Esta es la función que generá todas las posibles jugadas para un juego en concreto.\n
            La implementación de este algoritmo no incorporá actualmente ninguna de las
            optimizaciones de performance clásicas para árboles MiniMax.\n
            Esta función generará todos los nodos/momentos/movimientos que conforman el
            juego actual en concreto, y luego realizará calculos para determinar su valor
            heurístico y otros estados de los nodos que conforman el cerebro de este jugador.\n
            Cabe resaltar, que los nodos instanciados en esta clase, en esta función son totalmente
            PARTICULARES de la instancia. Siendo que los nodos tendrán valores calculados, en orden y valor,
            en base a este jugador.\n
            El accionar de esta función se puede resumir en los siguientes pasos:\n
            \t1. Primero se tendrá una clausula de terminación de recursión (puesto que esta clase fue implementada
            para su uso recursivo)\n
            \t2. En caso de que no se accede a la clausula de terminación, en principio se generarán todos los
            nodos/momentos/jugadas en base a las manos recibidas como parámetro. Es importante tener en cuenta,
            que los parámetros `current_values` y `next_moves` representan las manos del jugador actual y
            del proximo jugador, esto nos dice que es importante la correcta elección de estas 2 variables
            en el momento de callear esta función.\n
            \t3. Antes de moverse a la evaluación heurística, durante la creación de los nodos, se les asignará
            (en caso de aplicar) el jugador que gana en este momento, y se actualizan sus valores de victoria y derrota,
            siempre conforme a esta instancia\n
            \t4. Una vez creados todos los movimientos, se aplica el calculo heurístico sobre la raiz actual
            en base a sus hijos, también se actualizan las métricas de win y lose en la raiz actual.\n

            Args:
                root (Node): Durante el calleo, será la raiz inicial; durante las llamadas recursivas
                    tomará el papel de nodo/raiz actual
                current_moves (list): mano del jugador actual
                next_moves (list): mano del proximo jugador
                depth (int): profundidad en el árbol, generlamente se la incializa en 0 durante el calleo.
                    Este valor será análogo al turno actual durante un juego
                how_moves (str): Id del jugador actual (no de la instancia), este valor se va alternando
                    dependiendo quien haya movido
                limit (int): Limite actual, es utilizado para actualizar los valores de win/lose. Durante el calleo
                    se lo setea como el limite máximo que se impondrá en el juego
        """
        if not current_moves:
            # Llegue a una hoja
            root.how_wins = 'n/a'  # No hay ganador
            root.heuristic_value = 0
            return
        # Analizo los siguientes movimientos actuales
        for i, actual_move in enumerate(current_moves):
            # Calculo las variables para el proximo turno
            next_current_moves = copy.deepcopy(current_moves)
            del next_current_moves[i]  # Saco al movimiento actual de la lista de movimientos, ya que la proxima vez que le toque al dueño de esta lista, no podrá volver a elegir el movimiento actual
            new_limit = limit - actual_move  # Calculo el nuevo limite (le resto la carta que se acaba de tirar (actual_move))
            actual_depth = depth + 1  # Bajamos 1 nivel en el árbol
            new_to_move = 'p1' if how_moves is 'p2' else 'p2'  # Calculo a quien le toca en el proximo turno (== proxima llamada recursiva)
            
            # Calculo la proxima raiz
            current_node = Node(actual_move, new_limit, actual_depth, how_moves)  # Nodo del movimiento actual
            root.add_child(current_node)  # Guardo el movimiento actual como uno de los posibles movimientos de la raiz
            self.__all_nodes.append(current_node)

            if new_limit < 0:  # Significa que el jugador actual se pasó del limite, por lo tanto pierde
                player_how_wins = 'p1' if how_moves is 'p2' else 'p2'
                current_node.how_wins = player_how_wins # Seteo al ganador en la jugada actual, como el jugador contrario al que esta moviviendo ahora
                current_node.heuristic_value = self.VALUES[player_how_wins]
                current_node.wins += 1 if player_how_wins == self.who_am_i else 0
                current_node.loses += 1 if player_how_wins != self.who_am_i else 0
            else:  # Todavía no se superó el limite, por lo tanto es el turno del proximo jugador
                self.simulate_moves(current_node, next_moves, next_current_moves, actual_depth, new_to_move, new_limit)  # Calculo la proxima jugada, cambiando

        # Hora de la lógica para el MiniMax...
        if how_moves == self.who_am_i:  # Jugador a maximizar sus posibilidades de ganar
            heuristic_evaluation = float('-inf')
            for child in root.childs:
                heuristic_evaluation = max(heuristic_evaluation, child.heuristic_value)
                root.wins += child.wins
                root.loses += child.loses
        else:  # Jugador a minimizar sus posibilidades de ganar
            heuristic_evaluation = float('inf')
            for child in root.childs:
                heuristic_evaluation = min(heuristic_evaluation, child.heuristic_value)
                root.wins += child.wins
                root.loses += child.loses
        root.heuristic_value = heuristic_evaluation

    def _get_brain_as_text(self, root: Node, q_tabs: int = 0, data: str = '') -> str:
        """
            Esta función devuelve un string que contendrá datos básicos sobre cada nodo.\n
            Para esto se realiza un recorrido que guardará primero a la raiz actual y luego
            irá añadiendo los resultados de los nodos hijos.
            El estado que devuelve esta función es utilizado para generar la vista en tiempo
            real de las posibles decisiones del jugador CPU.
            La distinción de los diferentes niveles se emulará con valores \\t (tabs).

            Args:
                root (Node): Durante el calleo es la raiz desde la que se quiere comenzar a
                    dumpear el estado; durante las llamadas recursivas representa la raiz actual
                q_tabs (int): Cantidad de tabs por recursión
                data (str): Al momento del calleo, su valor por defecto es nulo; durante las llamadas
                    recursivas irá alojando los valores que devuelven sus descendientes

            Returns:
                str: Dump basado en una raiz en concreto                
        """
        tabbing = '\t' * q_tabs
        if not root.childs:
            return f'\n{tabbing} Node: <{root.data}> ; h_value: <{root.heuristic_value}> ; how_plays: <{root.how_moves}> ; how_wins: <{root.how_wins}> ; win-lose: {root.wins} - {root.loses} ; win_rate: {root.win_rate}%'
        else:
            aux = f'\n{tabbing} Node: <{root.data}> ; h_value: <{root.heuristic_value}> ; how_plays: <{root.how_moves}> ; how_wins: <{root.how_wins}> ; win-lose: {root.wins} - {root.loses} ; win_rate: {root.win_rate}%'
            for child in root.childs:
                aux += self._get_brain_as_text(child, q_tabs+1, data)

            return data + aux

    def dump_brain(self):
        """
            Esta función será la encargada de ir dumpeando el estado desde la raiz
            actual del juego, a unn archivo externo que podrá utiliar el backend
            para visualizarnos el cerebro del jugador CPU
        """
        with open(self.dump_dir, 'w', encoding='utf-8') as file_buffer:
            data = self._get_brain_as_text(self.current_game_root)
            file_buffer.write(data)
