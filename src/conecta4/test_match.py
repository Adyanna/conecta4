from .player import Player, HumanPlayer
from .match import Match

#None para qu existan las variables globables
xavier = None
otto = None

#se ejecuta antes de cada uno de los test
def setup_function():
    #con global llamamos a la variable creada 
    global xavier
    xavier = HumanPlayer('Prof. Xavier')
    global otto
    otto = Player("Dr. Octopus")

#se ejecuta DESPUES de cada uno de los test
def teardown_function():
    global xavier
    xavier = None
    global otto
    otto = None

def  test_different_players_have_differente_chars():
    t = Match(xavier,otto)
    assert xavier.char!=otto.char

def test_no_player_with_None_char():
    t=Match(xavier,otto)
    assert xavier.char is not None
    assert otto.char is not None

def test_next_player_is_round_robbin():
    t=Match(otto,xavier)
    
    p1=t.next_player
    p2=t.next_player
    assert p1!=p2

def test_players_are_opponets():
    t = Match(otto,xavier)
    p1=t.next_player
    p2=t.next_player

    assert p1.opponent == p2
    assert p2.opponent == p1
    