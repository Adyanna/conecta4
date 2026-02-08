
from typing import Any

def find_streak(haystack, needle, streak):
  """
  Encuentra un racha de 
  """
  assert streak>0
  contador=0
  for item in haystack:
    if item==needle:
      contador+=1
      if contador==streak:
        break
    else:
      contador=0

  return contador==streak

def get_nths(lol: list[list[str | None]],n):
  """
  Recibe una lista de listas y devuelve una lista
  con los enesiomos elementos de la original
  """
  assert n>=1
  nths = []
  for sublist in lol:
    if len(sublist) < n:
      nths.append(None)
    else:
      nths.append(sublist[n-1])
  return nths

def tranpose_matriz(lol_m):
  """
  Recibe una matriz y devuelve su transpuesta
  """
  matrix = []
  #if is_matriz(lol_m):
  for i in range(0,len(lol_m[0])):
      new = get_nths(lol_m,i+1)
      if new != None:
        matrix.append(new)
  return matrix



def extend_list(elements: list, distance: int,distance_back:int, filler: Any)-> list:
    """
    Recibe una lista, la cual extiende en el inicio y por el final con distance filler
    No destructiva
    """
    return ([filler] * distance_back) + elements + ([filler] * distance)
      

def extend_lol(lol: list[list], filler: Any)-> list[list]:
    """
    Aplica extend_list a cada sublista del lol y me devuelve un nuevo lol
    con los campos desplazados 
    """
    new_lol = []
    lenthlol=len(lol)-1
    for index,val in enumerate(lol):
      new_list = extend_list(val,index,lenthlol-index,filler)
      new_lol.append(new_list)

    return new_lol

def reverse_list(l):
  return list(reversed(l))

def reverse_matrix(lol:list[list]):
  m = []
  for list_ in lol:
    m.append(reverse_list(list_))
  return m

def all_same(lol:list):
  same=True
  if lol!=[]:
    aux = lol[0]      
    for val in lol:
      if aux!=val:
        same=False
        break
  return same

#VALIDAMOS QUE UNA CADENA SEA UN NUMERO VALIDO
def is_int(data):
    try:
            num = int(data)
            return True
    except:
            return False
    
def collapse_list(list_:list[str|None],empty='.')->str:
    """
    Concatena todas las cedenas de la lista en una sola lista
    """
    val=""
    for char in list_:
        val += empty if char==None else char

    return val

def collapse_matrix(lol:list[list[str|None]], fence='|',empty='.')->str:
    """
    Concatena todas las cadenas en una sola separada por |
    """
    val=""
    for list_ in lol:
        val += collapse_list(list_,empty)+fence

    return val[:-1]

def explode_string(string_:str,dot=None):
   """
   Tranforma una cadena en una lista de caracteres
   """
   return list(string_)

def explode_list_of_string(list_of_string,dot=None):
    """
    Aplica explode_strign a cada cadena de la lista
    """
    result=[]
    for char in list_of_string:
        result.append(explode_string(char))
    return result

def replace_all_in_list(list_,char1,tochar2):
    new=[]
    for char in list_:
        new.append(tochar2 if char == char1 else char)
    return new
      
def replace_all_in_matriz(lol,char1, tochar2):
    new=[]
    for list_ in lol:
      new.append(replace_all_in_list(list_,char1,tochar2))
    return new


      


