

from .board import Board
from .player import Player
from .oracle import BaseOracle,ColumnRecommendation,ColumnClassification,SmartOracle
from .settings import BOARD_COLUMNS


def test_base_oracle():
    #d_or = BaseOracle()
    a = Player("Adr","x")
    board = Board.from_list([[None,None,None,None],
                             ['x','o','x','o'],
                             ['o','o','x','x'],
                             ['o',None,None,None]])
    
    expected = [ColumnRecommendation(0,ColumnClassification.MAYBE),
                ColumnRecommendation(1,ColumnClassification.FULL),
                ColumnRecommendation(2,ColumnClassification.FULL),
                ColumnRecommendation(3,ColumnClassification.MAYBE)]
    rappel = BaseOracle()

    assert len(rappel.get_recommendation(board,a))==len(expected)
    assert rappel.get_recommendation(board,a)== expected


def test__play_on_temp_board():
    winner = Player("Adr","x")
    loser = Player("Otto","o")

    empty = Board.from_list([[None,None,None,None],
                              [None,None,None,None],
                             [None,None,None,None],
                             [None,None,None,None]])
    #print(before)
    almost = Board.from_list([[None,None,None,None],
                              ['x','o',None,None],
                             ['x','o',None,None],
                             [None,None,None,None]])
    
    oracle = SmartOracle()

    #sobre tablero vacio
    for i in range(0,BOARD_COLUMNS-1):
        assert oracle._is_winning_move(empty,i,winner) == False
        assert oracle._is_winning_move(empty,i,loser) == False

    #sobre tablero almost
    for i in range(0,BOARD_COLUMNS-1):
        assert oracle._is_winning_move(almost,i,loser) == False


    assert oracle._is_winning_move(almost,0,winner)

def test_is_losing_move():
    winner = Player("Adr","x")
    loser = Player("Otto","o",opponent=winner)
    almost = Board.from_list([[None,None,None,None],
                              ['x',None,None,None],
                             ['o','o',None,None],
                             [None,None,None,None]])
    oracle = SmartOracle()
    oracle._is_losing_move(almost,0,winner) 
    oracle._is_losing_move(almost,1,winner) 
    oracle._is_losing_move(almost,2,winner)==False 
    oracle._is_losing_move(almost,3,winner) 

def test_no_good_option():
    p1 = Player("Adr",char="x")
    p2 = Player("Otto",char="o",opponent=p1)

    oracle = SmartOracle()
    maybe = Board.fromBoardRawCode('....|o...|....|....')
    bad_and_full = Board.fromBoardRawCode('x...|oo..|o...|xoxo')
    all_bad = Board.fromBoardRawCode('x...|oo..|o...|....')

    #ESTA MAL
    assert oracle.no_good_option(maybe,p1) == False
    assert oracle.no_good_option(bad_and_full,p1)
    #No funciona
    assert oracle.no_good_option(all_bad,p1)