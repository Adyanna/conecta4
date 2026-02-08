from .board import Board
from .oracle import BaseOracle,ColumnRecommendation,ColumnClassification,LearningOracle
from random import choice
from .list_utils import all_same,is_int
from .move import Move
from .settings import DEBUG,BOARD_COLUMNS
from beautifultable import BeautifulTable

class Player:
    """
    Representa un jugador, con un nombre y un caracter (con el que juega)
    """
    def __init__(self, name:str,char=None,opponent=None,oracle = BaseOracle())->None:
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent=opponent
        self.last_moves = []

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
    def play(self,board:Board):
        """
        Obtenemos la recomendacion del oraculo para posteriomente realizar la jugada de la maquina 
        """
        while True:
            try:
                #pregunto al oraculo
                (best,recommendations,help) = self._ask_oracle(board)
                #juego en la mejor 
                if help:
                    self.display_recommendations(board)
                    #self._list_of_recommendatios(board)
                elif not help:
                    self._play_on(board,best.index,recommendations)
                    break
            except ValueError as e:
                print(f"\n{e}")
                print("\n Intenta otra vez!")
        
        
    def _ask_oracle(self, board:Board):
        """
        Pregunta al oraculo y devuelve la mejor opcion
        """
        lrecomm = BaseOracle()
        list_recom = lrecomm.get_recommendation(board,self)
        best = self._choose(list_recom)
        return (best,list_recom,False)

    def _play_on(self,board:Board,position:int,recommendations:ColumnRecommendation):
        if DEBUG:
            self.display_recommendations(board)

        board.play(self.char,position)
        #guardamos la ultima jugada al principio de la lista
        self.last_moves.insert(0,Move(position,board.as_code(),recommendations,self))
        

    def _choose(self,recommendations: "ColumnRecommendation"):
        """
         selecciona la mejor opcion de la lista de recomendaciones
        """
        val = None
        lbest = list(filter(lambda x: x.classification != ColumnClassification.FULL, recommendations))
        #ordenamos por el orden decreciente
        lbest = sorted(lbest,key=lambda x:x.classification,reverse=True)
        if all_same(lbest):
             val = choice(lbest)
        else:
             val = lbest[0]
        return val
    
    def on_win(self):
        pass

    def on_lose(self):
        pass
    
    def display_recommendations(self, board:Board):
        #no guarda el WIN, guarda su valor
        data = map(lambda x: str(x.classification).split('.')[0].lower(), self._oracle.get_recommendation(board, self))
        tabla = BeautifulTable()
        tabla.rows.append(data)
        tabla.columns.header = [str(i) for i in range(BOARD_COLUMNS)]
        print(tabla)


#AQUI JUEGA EL PLAYER HUMANO
class HumanPlayer(Player):

    def __init__(self, name, char=None):
        super().__init__(name, char)

    def _ask_oracle(self, board):
        """
        Le pido al humano, que ingrese su jugada, o digite h para solicitar ayuda
        """
        while True:
            #pedido la columna
            val = input("Select a column (or h for help): \n").strip()
            #verificaod que su respuesta cumpla las condiciones
            resp = None
            if val=='h':
                resp = (ColumnRecommendation(None,None),None,True)
            elif is_int(val):
                #si no los es,jugamos
                value = int(val)
                resp = (ColumnRecommendation(value,None),None,False)
                
            return resp
        
class ReportingPlayer(Player):

    def on_lose(self):
        """
        le pide al oraculo que revise sus recomendaciones
        """
        #board_code =  self.last_moves.board_code
        #position = self.last_moves.position
        #self._oracle.update_to_bad(board_code,self,position)
        self._oracle.backtrack(self.last_moves)


