from pyfiglet import Figlet
from enum import Enum,auto
from .match import Match
from .player import Player,HumanPlayer
from .board import Board
from .list_utils import reverse_matrix
from beautifultable import BeautifulTable
from .settings import BOARD_COLUMNS
from .oracle import SmartOracle,BaseOracle,LearningOracle

class RoundType(Enum):
    COMPUTER_VS_COMPUTER=auto()
    COMPUTER_VS_HUMAN = auto()

class DifficultyLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HARD= auto()

class Game:

    def __init__(self, round_type=RoundType.COMPUTER_VS_COMPUTER,match=Match(Player('Chip'),Player('anse'))):
        self.round_type = round_type
        self.match = match
        self.board = Board()

    
    def start(self):
        #iniciamos el juego
        #imprimimos el logo del juego
        self.print_logo()
        #configuramos la partida
        self._configure_by_user()
        #arranco el game loop
        self._start_game_loop()
        

    def print_logo(self):
        f = Figlet(font='slant')
        print(f.renderText('Conecta4'))

    def _configure_by_user(self):
        """
        Le pido al usuario, los valores que el quiere para el tipo de partida, incluye la dificultad
        """
        #tipo de partida
        self.round_type = self._get_round_type()
        #seleccionamos el nivel de dificultad
        if self.round_type==RoundType.COMPUTER_VS_HUMAN:
            self._difficulty_level = self._get_difficulty_level()

        #crear la partida
        self.match = self._make_match()

    def _get_round_type(self):
        """
        preguntamos al usuario
        """
        print("""
            Select type of round:
              1) Computer vs Computer
              2) COmputer vs Human
        """)
        type_r=None
        response = ""
        while response != "1" and response!="2":
            response = input("Please type either 1 or 2: \n")

        if response =='1':
            type_r = RoundType.COMPUTER_VS_COMPUTER
        else:
            type_r = RoundType.COMPUTER_VS_HUMAN

        return type_r
    
    def _make_match(self):
        """
        Player 1 siempre sera robotico, asignamos la dificultad del juego.
        """
        _levels = {DifficultyLevel.LOW: BaseOracle(),DifficultyLevel.MEDIUM:SmartOracle(),DifficultyLevel.HARD:LearningOracle()}
        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            player1=Player("T-1000",oracle=LearningOracle())
            player2=Player("T-800",oracle=LearningOracle())
        else:
           player1=Player("T-3000",oracle=_levels[self._difficulty_level])
           player2= HumanPlayer(name=input('Enter your name: \n'))

        return Match(player1,player2)
    
    def _start_game_loop(self):
        """
        Iniciamos el bucle del juego
        """
        while True:
            #pedir el juego al jugador de turno
            current_player=self.match.next_player

            current_player.play(self.board)
            #mostrar su jugada
            self.display_move(current_player)
            #imprimo el tablero
            self._display_board()
            #si el juego termino
            if self._has_winner_or_tie():
                #mostrar resultado final
                self._display_result()
                #salgo del ducle
                if self.match.is_math_over():
                    break
                else:
                    self.board=Board()
                    self._display_board()

    def display_move(self,player:Player):
        """
        Mostramos en pantalla, el nombre, caracter y el movimiento del juegador
        """
        print(f'\n{player.name} ({player.char}) has moved in column {player.last_moves[0].position}. ')

    def _display_board(self):
        """
        Se utliza la libreria beautifultable para poder mostrar la tabla y sea agradable a la mista del jugador
        """
        m = self.board._columns
        m = reverse_matrix(m)
        # crear tabla con beautifultable
        bt = BeautifulTable()
        for i in m:
            bt.columns.append(i)
        bt.columns.header = [str(i) for i in range(BOARD_COLUMNS)]
        print(bt)

    def _display_result(self):
        """
        Imprime el nombre y caracter del ganador y en caso que sea un empate
        """
        winner = self.match.get_winner(self.board)
        if winner.char!=None:
            print(f"\n {winner.name} ({winner.char}) Wins!!")
        else:
            print(f'\nA tie between {self.match.get_player("x").name} and {self.match.get_player("x").name}')

    def _has_winner_or_tie(self):

        """
        El juego se acaba cuando hay vencedor o empate
        """
        #return self.board.is_victory(self.match.get_player()) mal
        result = False
        winner = self.match.get_winner(self.board)
        if winner != None:
            winner.on_win()
            winner.opponent.on_lose()
            result = True
        elif self.board.is_full():
            result = True

        return result
    

    def _get_difficulty_level(self):
        """
        pregunta la humanos que nivel de deficulta quiere, esto indica que tan inteligente sera la maquina
        """
        print("""
        Choose your opponent:
              1) Bender:for clowns and wimps
              2) T-800: you may regret it
              3) T-3000: Don't even think about it!
            """)
        level = None
        while True:
            responde = input("Please type 1, 2 or 3: \n").strip()
            if responde == '1':
                level = DifficultyLevel.LOW
                break
            elif responde == '2':
                level = DifficultyLevel.MEDIUM
                break
            else: 
                level = DifficultyLevel.HARD
                break

        return level

        