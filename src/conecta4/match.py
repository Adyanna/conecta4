from .player import Player
from .board import Board

class Match:

    def __init__(self,player1:Player,player2:Player):
        player1.char = 'x'
        player2.char = 'o'
        player1.opponent = player2

        self._players = {'x':player1,'o':player2}
        self._round_robbin = [player1,player2]
    
    @property
    def next_player(self):
        next = self._round_robbin[0]
        self._round_robbin.reverse()
        return next
    
    def get_player(self,char):
        return self._players[char]
    
    def get_winner(self,board:Board):
        """
        Devuelve el jugador ganador y si no lo hay, devuelve None
        """
        result = None
        if board.is_victory('x'):
            result=self.get_player('x')
        elif board.is_victory('o'):
            result = self.get_player('o')

        return result

    def is_math_over(self):
        """
        Pregunta al usuario si quiere otra partida
        """
        resp = True
        while resp:
            answer = input("Would you like another match? (Y/N): \n").upper()
            if answer =='Y':
                resp = False
                break
            elif answer == 'N':
                resp = True
                print("See you later, have a good day!")
                break
        return resp
    



