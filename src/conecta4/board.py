from conecta4.settings import BOARD_COLUMNS, BOARD_ROWS, VICTORY_STREAK
from .list_utils import find_streak,tranpose_matriz,extend_lol,reverse_matrix
from copy import deepcopy


type MatrixColumn = list[list[str|None]]

class Board:
    """
    Representa un tablero con las dumensiones de settings
    detecta una victoria
    """

    #metodos de clase
    @classmethod
    def from_list(cls,list_repr:MatrixColumn):
        board = cls()
        board._columns = deepcopy(list_repr)
        return board

    #DUNDERS
    def __init__(self)-> None:
        """
        Crea un tablero con las dimenciones adecuadas
        El tablero es una "Matriz" (lista de listas), de caracteres de jugador
        y None representa una posicion vacia
        """
        #self.columns = [[None]*BOARD_ROWS]*BOARD_COLUMNS  #bugggggg\
        self._columns: list[list[str|None]] = []

        self._columns = [[None for i in range(BOARD_COLUMNS)] for j in range(BOARD_ROWS)]
        #iniciar un for 
        """
        for col_num in range(BOARD_COLUMNS): #Columna
            self._columns.append([])
            for row_num in range(BOARD_ROWS): #Fila
                self._columns[col_num].append(None)
        """
        #for column_row in 

    #DOS OBJETOS EQUIVALENTES, TIENE QUE TENER EL MISMO HASH
    def __eq__(self, value: object)->bool:
        """
        se ejecuta cuando haces a == b
        siendo a 'self ' y b 'value'
        """
        result = True
        if not isinstance(value,self.__class__):
            result = False
        else:
            # son de la misma clase: comparo sus propiedades
            # en este caso, _columns
            result=(self._columns == value._columns)
        
        return result  
    
    #NO PUEDO MTER DATOS MUY GRANDES, TENGO QUE COMPRIMIRLOS
    def __hash__(self)->int:
        return hash(self._columns)
    
    def __repr__(self)->str:
        """
        Devuelve represetnacion textual del objeto: las columnas
        """
        return f"{self.__class__}: {tranpose_matriz(self._columns)}>"
    
    def __len__(self):
        return len(self._columns)
    
    # CREAR UNA FUNCION BOARDCODE
    #QUE TRANFORMA LA MATRZI EN STRIGN
    #DIVIDE Y VENCES, UNA LISTA EN CADENA

    #INTERFAZ PUBLICA
    
    def play(self, player_char:str, col_numer:int)->None:
        """
        Metodo impuro, solo lleva a  cabo efecto secundario 
        (cambia el tablero)
        si col_number no es valido, debe de lanzar excepcion
        ValueError si la comumna esta llena o si el indice es de una columna inexistente
        """
        try:
            #validar que se encuentre en rango 
            col = self._columns[col_numer]
            found_slot = False 
            for index,item in enumerate(col):
                if item==None:
                    found_slot=True
                    col[index]=player_char
                    break
            if not found_slot:
                #Valida si la columna esta vacia
                raise ValueError(f"La columna {col_numer}, esta llena!")
        except IndexError:
            raise ValueError(f"{col_numer} no es valida")
  

    def is_victory(self,player_chat:str)->bool:
        """
        Determina si hay una victoria para el jugador, representado por un caracter
        """
        return self._has_vertical_victory(player_chat,self._columns) or self._has_horizontal_victory(player_chat) or self.has_ascending_victory(player_chat) or self.has_descending_victory(player_chat,self._columns)
    
    def is_tie(self,char1,char2):
        return not self.is_victory(char1) and not self.is_victory(char2)
    
    def is_column_full(self, index):
        return self._columns[index][BOARD_ROWS - 1] is not None
    
    def is_full(self):
        result = True
        for i,data in enumerate(self._columns):
            result= self.is_column_full(i) and result

        return result
    

    #interfaz privada
    #estos son funciones que nadie mas puede tener y se representan con "_" guion bajo

    #tarea
    def _has_vertical_victory(self,player_char:str,Matriz:list[list[str|None]])->bool:
        result =  False
        for column in Matriz:
            result = find_streak(column,player_char,VICTORY_STREAK)
            if result:
                break
        return result
    
    #tarea
    def _has_horizontal_victory(self,player_char:str)->bool:#matrix: list[list[str|None]]
        temporal = Board.from_list(self._columns)
        transpose = tranpose_matriz(temporal._columns)
        return self._has_vertical_victory(player_char,transpose)
    
    def has_ascending_victory(self,player_char:str)->bool: #,matrix:list[list[str|None]]
        temporal = Board.from_list(self._columns)
        rm = reverse_matrix(temporal._columns)
        #print(rm)
        return self.has_descending_victory(player_char,rm)
    
    def has_descending_victory(self,player_char:str, matrix:list[list[str|None]])->bool: 
        temporal = Board.from_list(matrix)
        return self._has_vertical_victory(player_char,tranpose_matriz(extend_lol(temporal._columns,None)))
    

