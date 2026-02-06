from enum import Enum, auto
from .board import Board
from .player import *
from .settings import BOARD_ROWS,BOARD_COLUMNS
from copy import deepcopy
#from typing import TYPE_CHECKING

#if TYPE_CHECKING:
#    from .player import Player

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
        #si son de lamisma clase, pos comparto las propiedades de uno y otro
        else:
            return (self.index,self.classification)==(other.index,other.classification)
    
    def __hash__(self)->int:
        return hash(self.index,self.classification)

    # Oraculos, de mas tonto a las listo
    # Los oraculos, deben de realizar un trabajo complejo: clasificar columnas
    # en el caso mas complejo, teniendo en cuenta errores del pasado
    # Usamos divide y venceras, donde cada oraculo del mas tonto al mas listo
    # Se encargara de una parte

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
            #se puede mejorar
            # creo un table temporal a partir de board
            # juego en index
            temp_board = self._plat_on_temp_board(board,index,player)
            # le pregunto al tablero temporal si is_victory(player)
            if  temp_board.is_victory(player.char):
                recommendation.index = index
                #si es asi, reclasifico a WIN
                recommendation.classification = ColumnClassification.WIN
        return None
    
    def _play_on_temp_board(self,original:Board,index:int,player:"Player")->Board:
        """
        Crea una copia(profunda) del board original juega en nombre de player, en al columna que nos han dicho y devuleve el board resultante
        """
        new_board = deepcopy(original)
        new_board.play(player.char,index)
        return new_board





        
