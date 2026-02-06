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

