from .game import Game
from .board import Board


def test_creation():
    g = Game()
    assert g is not None

def test_is_game_over():
    game = Game()
    won_x = Board.from_list([[None,None,None,None],
                             ['x','o','x','o'],
                             ['o','x','x','x'],
                             ['o',None,None,None]])
    won_o = Board.from_list([[None,None,None,None],
                             ['x','o','x','o'],
                             ['o','o','o','x'],
                             ['o',None,None,None]])
    tie = Board.from_list([['o','x','o','x'],
                             ['x','o','x','o'],
                             ['o','o','o','x'],
                             ['o','x','x','o']])
    undinished = Board.from_list([['x','o','x','o'],
                                [None,None,None,None],
                             [None,None,None,None],
                             [None,None,None,None]])
    game.board = won_x
    assert game._has_winner_or_tie()==True

    game.board = won_o
    assert game._has_winner_or_tie()==True

    game.board = tie
    assert game._has_winner_or_tie()==True

    game.board = undinished
    assert game._has_winner_or_tie()==False
