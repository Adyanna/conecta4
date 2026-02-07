from enum import Enum, auto
from .board import Board
from .player import *
from .settings import BOARD_ROWS,BOARD_COLUMNS
from copy import deepcopy

class ColumnClassification:
    FULL = -1 # Imposible
    LOSE = 1 # Derrota inminente
    BAD = 5 # Muy indeseable
    MAYBE = 10 # Indeseable
    WIN = 100 # Victoria inmediata

class ColumnRecommendation:

    #contructor
    def __init__(self, index: int, classification:ColumnClassification)->None:
        #propiedades
        self.index = index  #objeto
        self.classification = classification

    def __eq__(self, other):
        #si son de clases distintas, pues distintos
        if not isinstance(other,self.__class__):
            return False
        else:
            #si son de la misma clase,comparando solo la clasificacion
            return self.classification==other.classification
    
    def __hash__(self)->int:
        return hash(self.index,self.classification)

# Oraculos, de mas tonto a las listo
# Los oraculos, deben de realizar un trabajo complejo: clasificar columnas
# en el caso mas complejo, teniendo en cuenta errores del pasado
# Usamos divide y venceras, donde cada oraculo del mas tonto al mas listo

#desiende de objet asi que no se especifica () el padre
class BaseOracle:
    """
    La clase base y el oraculo mas tonto: clasifica las columnas en llenasy no llenas
    no se necesita init:
    """
    def get_recommendation(self, board:Board,player:"Player")-> list[ColumnRecommendation]:
        """
        Retorna una lista de recomendaciones
        """
        recommendations = [] #por ahora , full o maybe 
        for index in range(BOARD_COLUMNS):
            recommendations.append(self._get_column_recommendation(board,index,player))
        return recommendations
    
    # metodo privado
    def _get_column_recommendation(self, board: Board,index:int,player: "Player")-> ColumnRecommendation:
        """
        Metodo privado, que determina si una columna esta llena, en cuyo caso la clasifica como FULL.
        para todo lo demas, MAYBE.
        """
        result = ColumnRecommendation(index,ColumnClassification.MAYBE)

        #comprueba si me he equivocado y si es asi, cambio el valor de result 
        if board.is_column_full(index):
            result = ColumnRecommendation(index,ColumnClassification.FULL)
        return result


class SmartOracle(BaseOracle):
    """
    Refina la reomendacion del oraculo base, intentando afinar la clasificacion, MAYBE a algo mas preciso.
    En concreto a WIN: va a determinar que jugadas nos llevan a ganar de inmediato
    """
    def get_column_recommendation(self, board:Board, index: int, player: "Player")-> ColumnRecommendation:

        #pido la clasificacion basica
        recommendation = super()._get_column_recommendation(board, index, player)
       
        # afino los Maybe: juego como player en esa ccolumna y compruebo si eso me da una victoria 
        if recommendation.classification == ColumnClassification.MAYBE:
            # le pregunto al tablero temporal si is_victory(player)
            if  self._is_winning_move(board,index,player):
                #si es asi, reclasifico a WIN
                recommendation.classification = ColumnClassification.WIN
                recommendation.index = index
            elif self._is_losing_move(board,index,player):
                recommendation.classification = ColumnClassification.LOSE
                recommendation.index = index

        return recommendation
    
    def _play_on_temp_board(self,original:Board,index:int,player:"Player")->Board:
        """
        Crea una copia(profunda) del board original juega en nombre de player, en al columna que nos han dicho y devuleve el board resultante
        """
        new_board = deepcopy(original)
        new_board.play(player.char,index)
        return new_board
    
    def _is_winning_move(self,board:Board,index:int,player:"Player")->bool:
        """
        Determina si al jugar una posicion, nos llevaria a ganar de inmediato
        """
        temp = self._play_on_temp_board(board,index,player)
        return temp.is_victory(player.char)
    
    def _is_losing_move(self, board:Board,index:int,player:"Player")->bool:
        """
        Si player juega en index, genera una juegada vencedora para el oponente en alguna de las demas columnas?
        """
        will_lose = False
        temp = self._play_on_temp_board(board,index,player)
        for i in range(0,BOARD_COLUMNS-1):
            if self._is_winning_move(temp,i,player.opponent):
                will_lose = True
                break
        return will_lose

        
