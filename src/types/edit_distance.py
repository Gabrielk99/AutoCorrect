import numpy as np

class DynamicEditDistance():
  _insert_weight: float
  _delete_weight: float
  _replace_weight: float
  
  def __init__(self, insert_w:float, delete_w:float) -> None:
    """

    Args:
        insert_w (float): weight to insert process
        delete_w (float): weight to delete process
    """    
    self._insert_weight = insert_w
    self._delete_weight = delete_w
    self._replace_weight = self._insert_weight + self._delete_weight
    
  def __call__(self, word_l:str, word_r:str,debug:bool = False) -> int:
    """
    Compute the edit distance into two words
    Args:
        word_l (str): word source
        word_r (str): word target
        debug (bool): active the toString from D matrix
    Returns:
        int: return the edit distance
    """    
    word_l,word_r = "#"+word_l,"#"+word_r
    left_size , right_size = len(word_l)+1,len(word_r)+1
    dynamic_matrix = np.zeros((left_size,right_size))
    dict_word_l = {i:letter for i,letter in enumerate(word_l)}
    dict_word_r = {i:letter for i,letter in enumerate(word_r)}
    dynamic_matrix[0,:].fill(np.inf)
    dynamic_matrix[:,0].fill(np.inf)

    for i in range(1,left_size):
      for j in range(1,right_size):
        if i == 1 and j==1:
          continue 
        
        top = dynamic_matrix[i-1,j] + self._delete_weight
        left = dynamic_matrix[i,j-1] + self._insert_weight

        if dict_word_l.get(i-1,None) != dict_word_r.get(j-1,None):
          diag = dynamic_matrix[i-1,j-1] + self._replace_weight
        else :
          diag =  dynamic_matrix[i-1,j-1]
 
        dynamic_matrix[i,j] = min(top,left,diag)
        if debug:
          self.toString(word_l,word_r,dynamic_matrix)
        
    return dynamic_matrix[-1,-1]
    
  def toString(self,word_l:str,word_r:str,D):
    print("        ","   ".join(word_r))
    for i,letter in enumerate(" "+word_l):
      print(letter," ",D[i])
    