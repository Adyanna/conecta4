from .board import *
from .settings import *


def test_victory():
    b = Board()
    for i in range(VICTORY_STREAK):
        b.play('x',i)

    assert b.is_victory('o') == False
    assert b.is_victory('x') == True 

def test_tie():
    b = Board()
    b.play('o',0)
    b.play('o',1)
    b.play('x',2)
    b.play('o',2)
    assert b.is_tie('o','x')==True


def test_board_code():
    board = Board.from_list([['x',None,None,None],
                              ['x','o','x','o'],
                             ['x','o','x','x'],
                             ['o',None,None,None]])
    
    code = board.as_code()
    clone_board = Board.fromBoardCode(code)

    assert clone_board == board
    assert clone_board.as_code()==code
    assert clone_board.as_code().raw_code == code.raw_code