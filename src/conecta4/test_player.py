from .board import *
from .settings import *
from .player import *

def test_play():
    player = Player('Adri','x')
    before = Board.from_list([[None,None,None,None],
                              ['x','o','x','o'],
                             ['x','o','x','o'],
                             ['o',None,None,None]])
    #print(before)
    after = Board.from_list([['x',None,None,None],
                              ['x','o','x','o'],
                             ['x','o','x','x'],
                             ['o',None,None,None]])
    #print(after)


    matriz = player.play(before)
    print(matriz)
    #print(before._columns)
    #assert before==after #NO FUNCION
    