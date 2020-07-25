from game import exceptions

class HumanController:
    """
        Esta clase tiene la intención de funcionar como controlador
        para un posible jugador humano.\n
        El método `play_a_move()` es relativo al que se puede encontrar
        en el controlador de los jugadores CPU, tomando la ultima carta como
        referencia (aunque en este caso no de ningún valor agregado), luego pide
        que se realice un movimiento, en este caso, el descarte de una de las
        "cartas" que tenemos.

        Attributes:
            who_am_i (str): id del jugador
            my_cards (list): lista de cartas/valores que le fueron asignados
            alias (str): Nombre alternativo utilizado dentro del juego
                para referirse al mismo
    """
    def __init__(self, who_am_i: str, alias: str):
        self.who_am_i = who_am_i
        self.my_cards = []
        self.alias = alias

    def play_a_move(self, last_card: int):
        """
            Esta función es la llamada desde la rutina del juego.\n
            La misma pedirá al usuario que seleccione uno de las
            cartas/valores que le quedan disponibles, para añadir al
            monto global del juego.

            Args:
                last_card (int): Ultima carta jugada, esta representará siempre
                    el movimiento del otro jugador
            
            Returns:
                choice (int): Valor seleccionado por el usuario para descartar
        """
        print(f'Sus cartas actuales son: {self.my_cards}')
        while True:
            human_order = input('Ingrese su orden: ')
            try:
                human_order = int(human_order)
                if human_order in self.my_cards:
                    del self.my_cards[self.my_cards.index(human_order)]
                    return human_order
            except:
                print(f'El valor ingresado (<{human_order}>) no es valido')
            
