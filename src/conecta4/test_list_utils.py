from .list_utils import *
from .settings import *


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
