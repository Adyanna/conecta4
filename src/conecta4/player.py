
#from .board import Board
#from .oracle import BaseOracle, ColumnRecommendation, ColumnClassification

#from typing import TYPE_CHECKING

#if TYPE_CHECKING:
from .board import Board
from .oracle import *
class Player:
    """
    Representa un jugador, con un nombre y un caracter (con el que juega)
    """
    def __init__(self, name:str,char=None,opponent=None,oracle = BaseOracle())->None:
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent=opponent
        self.last_move = None

    @property
    def opponent(self):
         return self._opponent
    
    #tener cuidado de no utilizar el mismo, se crean bucles infinitos
    @opponent.setter
    def opponent(self,other):
         if other != None:
            self._opponent = other
            other._opponent = self

    #AQUI JUEGA LA MAQUINA
    def playmachine(self,board:Board):
    
        #pregunto al oraculo
        (best,recommendations) = self._ask_oracle(board)
        #juego en la mejor 
        self._play_on(board,best.index)
        
        
    def _ask_oracle(self, board:Board):
        """
        Pregunta al oraculo y devuelve la mejor opcion
        """
        lrecomm = BaseOracle()
        list_recom = lrecomm.get_recommendation(board,self)
        best = self._choose(list_recom)
        return (best,list_recom)

    def _play_on(self,board:Board,position:int):
        board.play(self.char,position)
        self.last_move=position
        

    def _choose(self,recommendations: "ColumnRecommendation"):
        
        #selecciona la mejor opcion de la lista de recomendaciones
        lbest = list(filter(lambda x: x.classification != ColumnClassification.FULL, recommendations))
        return lbest[0]
    
    #AQUI JUEGA EL PLAYER HUMANO

    
class HumanPlayer(Player):
    
    def __init__(self, name, char=None):
        super().__init__(name, char)

    def _ask_oracle(self, board):
        """
        Le pido al humano, que ingrese su jugada
        """
        while True:
            #pedido la columna
            val = input("Select a column: \n")
            #verificaod que su respuesta cumpla las condiciones
            if _is_int(val):
                #si no los es,jugamos
                pos = int(val)
                return (ColumnRecommendation(pos,None),None)

        

#VALIDAMOS QUE UNA CADENA SEA UN NUMERO VALIDO
def _is_int(data):
    try:
            num = int(data)
            return True
    except:
            return False
