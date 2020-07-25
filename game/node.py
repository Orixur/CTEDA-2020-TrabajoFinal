class Node:
    """
        Esta clase se propone funcionar como las componentes del árbol
        de decisiones del jugador CPU.\n
        También se puede interpretar uno de estos nodos como un estado
        posible del juego, teniendo el identificador de la persona que movió,
        la carta que movio, el turno, etc.\n
        Recordar que cada nodo es relativo al jugador en el cual se desarrollo
        el mapeo de movimientos (por ejemplo, el índicador de derrotas o victorias
        será relativo al jugador CPU que le pertenece este nodo).
        
        Attributes:
            data (int): Esta variable contendrá un valor númerico, el cual
                representará el valor de la "carta" descartada para este movimiento
            mount_count (int): monto en el momento de este nodo. El monto será un valor
                que siempre tenderá a 0.
            how_moves (str): Contendrá el id del jugador que generó este movimiento
            depth (int): Profundidad en el árbol, es también el analogo a "que turno",
                durante el transcurso de un juego
            wins (int): Valor númerico que puede ser 1, 0 o -1
            loses (int): Valor númerico que puede ser 1, 0 o -1
            childs (list): Lista de nodos, estos son los hijos mas inmediatos
            heuristic_value (int): Resultado de una evaluación heuristica para el
                nodo/movimiento actual
    """
    def __init__(self, data: int, mount_count: int, depth, how_moves: str = None):
        """
            Este constructor recibirá como parámetros los valores que describen
            la jugada/nodo actual.
        """
        self.data = data
        self.mount_count = mount_count
        self.how_moves = how_moves
        self.depth = depth
        self.wins = 0
        self.loses = 0
        self.childs = []
        self._how_wins = 'n/a'
        self.heuristic_value = None
    
    def add_child(self, node):
        self.childs.append(node)

    @property
    def win_rate(self) -> int:
        """
            Esta función devuelve el ratio de victoria que tendría el jugador
            CPU dueño de este nodo.\n
            Recordar que los contadores de victorias y derrotas son relativos
            al jugador dueño del nodo.

            Returns:
                int: Ratio de victoria en base a los hijos posteriores, es un valor
                    crucial para que los jugadores CPU puedan identificar cual es
                    la mejor jugada posible en el momento de la acción de descarte
        """
        try:
            return ((self.wins) * (100)) / (self.wins + self.loses)
        except ZeroDivisionError:
            return 'n/a'

    @property
    def how_wins(self):
        return self._how_wins
    
    @how_wins.setter
    def how_wins(self, value):
        self._how_wins = value
        
    def __repr__(self):
        return str(f'<Node with data: {self.data}>')
