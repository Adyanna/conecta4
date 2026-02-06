from conecta4.board import Board
from .player import Player
from .game import Game


if __name__ == "__main__":
    inicia = Game()
    inicia.start()



    """

    b = Board()
    a = Player("Adr","a")
    #print(b)
    b.play("X",0)
    b.play("Z",1)
    b.play("X",1)
    b.play("Z",2)
    b.play("Z",2)
    b.play("X",2)
    b.play("Z",3)
    b.play("X",3)
    b.play("Z",3)
    b.play("X",3)
    #print(b._columns)
    #print(b.has_descending_victory("X",b._columns))

    #print("get")
    #print(BaseOracle.get_column_recommendation(BaseOracle,b,3,a))
    #print(b.has_descending_victory("X"))

    #b2 = Board.from_list([['X',None,None,None],['Z','X',None,None],['Z','X','X',None],['Z','Z','Z','X']])

    #print(b==b2)
    #print(b is b2)
    
    c = Board()
    c.play("X",3)
    c.play("Z",2)
    c.play("X",2)
    c.play("Z",1)
    c.play("Z",1)
    c.play("X",1)
    c.play("Z",0)
    c.play("Z",0)
    c.play("X",0)
    #c.play("N",0)
    #print(c._columns)
    #print(c.has_ascending_victory('X'))

    #print(c._columns)
    #print
    



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


    matriz = player.playmachine(before)
    print(player.playmachine(before))
    print(before._columns)


"""


