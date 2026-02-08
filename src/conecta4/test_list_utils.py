from .list_utils import *
from .settings import *
from .oracle import ColumnClassification,ColumnRecommendation


#test de 
def test_find_streak():
    assert find_streak([1, 2, 3, 4, 5], 4, 2) == False
    assert find_streak([1, 2, 3, 4, 5], 42, 2) == False
    assert find_streak([1, 2, 3, 4], 4, 1)
    assert find_streak([1, 2, 3, 1, 2], 2, 2) == False
    assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 3)
    assert find_streak([5, 5, 5, 1, 2, 3, 4], 5, 3)
    assert find_streak([1, 2, 5, 5, 5, 3, 4], 5, 3)
    assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 4) == False

def test_get_nths():
    original = [[0, 7, 3], [4, 0, 1]]
    assert get_nths(original,1) == [0, 4]

def test_all_same():
    assert all_same([1,2,3,4])==False
    assert all_same([[],[],[]])
    assert all_same([])
    assert all_same([ColumnRecommendation(0,ColumnClassification.WIN),ColumnRecommendation(2,ColumnClassification.WIN)])
    assert all_same([ColumnRecommendation(0,ColumnClassification.MAYBE),ColumnRecommendation(2,ColumnClassification.WIN)]) == False

def test_collapse_list():
    assert collapse_list([])==""
    assert collapse_list(['x','s','a'])=='xsa'
    assert collapse_list(['x','s','a',None])=='xsa.'

def test_collapse_matrix():
    assert collapse_matrix([])==""
    assert collapse_matrix([['x','s','a'],['x','s','a'],['x','s','a']])=='xsa|xsa|xsa'
    assert collapse_matrix([['x','s','a',None],['x','s','a',None],['x','s','a',None]])=='xsa.|xsa.|xsa.'





def test_explode_string():
    assert explode_string("")==[]
    assert explode_string('xsa')==['x','s','a']
    assert explode_string('xsa.')==['x','s','a','.']

def test_explode_list_of_string():
    assert explode_list_of_string('')==[]
    assert explode_list_of_string(['xsa','xsa','xsa'])==[['x','s','a'],['x','s','a'],['x','s','a']]
    assert explode_list_of_string(['','',''])==[[],[],[]]

def test_replace_all_in_list():
    assert replace_all_in_list([],None,'#')==[]
    assert replace_all_in_list(['x','s','a',','],',',None)==['x','s','a',None]
    assert replace_all_in_list(['x','s','a',None],'.','X')==['x','s','a',None]

def test_replace_all_in_matriz():
    assert replace_all_in_matriz([],None,7)==[]
    assert replace_all_in_matriz([[],[]],None,7)==[[],[]]
    assert replace_all_in_matriz([[None,None,2,True],[1,2,'l']],'o',43)==[[None,None,2,True],[1,2,'l']]
    assert replace_all_in_matriz([[1,0,2,None],[1,2,None]],1,'b')==[['b',0,2,None],['b',2,None]]




