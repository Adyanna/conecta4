from enum import Enum, auto
from .board import Board,BoardCode
from .player import *
from .settings import BOARD_ROWS,BOARD_COLUMNS
from copy import deepcopy
from .move import Move

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
    
    def no_good_option (self,board:Board,player:"Player"):
        """
        Detecta que todas las clasificaciones sean BAD o FULL
        """
        ColumnRecommendation = self.get_recommendation(board,player)
        result = True
        for rec in ColumnRecommendation:
            if (rec.classification == ColumnClassification.WIN) or (rec.classification == ColumnClassification.MAYBE):
                result = False
                break
        return result
    
    #se anadie para que todos los oraculos tengan los mismo metodos
    #con el fin que si alguno necesita algo en especifico, como LearningOracle en este caso
    #pueda sobreescribirlo y no se tenga que anadir codigo para poder identificar el tipo de oraculo
    def update_to_bad(self, move: Move):
        pass
    def backtrack(self, list_of_moves:Move):
        pass

    
    # metodo privado
    def _get_column_recommendation(self, board: Board,index:int,player: "Player")-> ColumnRecommendation:
        """
        Metodo privado, que determina si una columna esta llena, en cuyo caso la clasifica como FULL.
        para todo lo demas, MAYBE.
        """
        result = ColumnRecommendation(index,ColumnClassification.MAYBE)
        #print(result)
        #comprueba si me he equivocado y si es asi, cambio el valor de result 
        if board.is_column_full(index):
            result = ColumnRecommendation(index,ColumnClassification.FULL)
        return result
    
class SmartOracle(BaseOracle):
    """
    Refina la reomendacion del oraculo base, intentando afinar la clasificacion, MAYBE a algo mas preciso.
    En concreto a WIN: va a determinar que jugadas nos llevan a ganar de inmediato
    """
    def _get_column_recommendation(self, board:Board, index: int, player: "Player")-> ColumnRecommendation:

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
    
class MemoizinOracle(SmartOracle):
    """
    El metodo get_recommedation, esta ahora memoizado, en donde cada vez que la llama, se guardan los parametros y el resultado
    en un diccionary
    """
    def __init__(self)->None:
        super().__init__()
        self._past_recommendations={}

    def _make_key(self,board:BoardCode,player:"Player"):
        """
        La clave convina el board y el player de la forma mas sensilla posible
        """
        return f"{board.raw_code}@{player.char}"

    def get_recommendation(self, board:Board, player:"Player"):
        """
        crea una clave y busca en las recomendaciones pasadas, caso contracion lo guarda en el diccionario
        """
        key = self._make_key(board.as_code(),player)
        if key not in self._past_recommendations:
            self._past_recommendations[key]=super().get_recommendation(board, player)
        return self._past_recommendations[key]
    
class LearningOracle(MemoizinOracle):

    def update_to_bad(self, move: Move):
        """
        Cambiamos la recomendacion de Maybe a Bad y se almacena en el diccionario
        """
        key = self._make_key(move.board_code,move.player)
        recommendation = self.get_recommendation(Board.fromBoardCode(move.board_code),move.player)
        recommendation[move.position] = ColumnRecommendation(move.position,ColumnClassification.BAD)
        self._past_recommendations[key] = recommendation
    
    def backtrack(self, list_of_moves: Move):
        """
        Repasa todas las jugadas y si encuentra una en la cual todo estaba perdido, se tiene que actualizar
        la anterior a BAD
        """
        #  NO ME FUNCIONA NO IMPRIME
        print("Learning... =D")
        for move in list_of_moves:
            self.update_to_bad(move)
            board = Board.fromBoardCode(move.board_code)
            if not self.no_good_option(board,move.player):
                break
        print(f"Size of knowledgebase: {len(self._past_recommendations)}")

