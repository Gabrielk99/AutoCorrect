from src.types.edit_distance import DynamicEditDistance
from src.types.vocabulary import Vocabulary

class AutoCorrect:
  
  _matrix_edit_calculator : DynamicEditDistance 
  _vocabulary: Vocabulary
  _mode: int 
  _n_suggestions:int
  
  def __init__(self,insert_w:float = 1.0,delete_w:float = 1.0,
               corpus:str = None, tokens:list = None, n_suggestions:int=5) -> None:
    self._matrix_edit_calculator = DynamicEditDistance(insert_w,delete_w)
    if corpus is not None:
      self._vocabulary = Vocabulary(corpus=corpus)
      self._mode = 0
    if tokens is not None:
      self._vocabulary = Vocabulary(collections=tokens)
      self._mode = 1
    
    self._n_suggestions = n_suggestions
    
  def __call__(self, word:str) -> list:
     #TODO
     pass