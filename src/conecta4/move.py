from .board import BoardCode
from .player import *
from .oracle import *

class Move:
    def __init__(self,position: int,board_code: BoardCode,recommendations:"ColumnRecommendation",player:"Player"):
        self.position = position
        self.board_code = board_code
        self.recommendations = recommendations
        self.player = player