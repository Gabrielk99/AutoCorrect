from src.types.edit_distance import DynamicEditDistance
from src.types.vocabulary import Vocabulary
from src.common.math import softmax
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from tqdm import tqdm
import itertools

def _apply_edit_distance(edit_distance:DynamicEditDistance,vocabulary:Vocabulary,
                        word:str,start:int,end:int)->dict:
  """Apply the edit distance on word and all words in vocabulary
      using a start and end signal point
      
      used in parallel process
  Args:
      edit_distance (DynamicEditDistance): Object that compute the edit distance
      vocabulary (Vocabulary): Object with vocabulary
      word (str): word to get distances
      start (int): start point to get words in vocab
      end (int): end point to get words in vocab

  Returns:
      dict: words and their scores
  """  
  dists = {word_voc:edit_distance(word,word_voc) 
           for word_voc in vocabulary._vocabulary[start:end]}

  return dists
  
class AutoCorrect:
  
  _matrix_edit_calculator : DynamicEditDistance 
  _vocabulary: Vocabulary
  _mode: int 
  _n_suggestions:int
  _n_editions:int
  _use_sub:bool
  def __init__(self,insert_w:float = 1.0,delete_w:float = 1.0,
               corpus:str = None, tokens:list = None, n_suggestions:int=5,
               n_editions:int=1,use_sub:bool=False) -> None:
    """constructor for autocorrect object
    
    AutoCorrect is a object that compute a simple edit distance 
    from some word to a specif vocabulary and return the most likely 
    words 

    Args:
        insert_w (float, optional): the insert cost. Defaults to 1.0.
        delete_w (float, optional): the delete cost. Defaults to 1.0.
        corpus (str, optional): corpus to build vocabulary. Defaults to None.
        tokens (list, optional): tokens to build vocabulary. Defaults to None.
        n_suggestions (int, optional): number of words to suggest. Defaults to 5.
        n_editions (int, optional): number of editions permissive. Defaults to 3.
        use_dub (bool, optional): if is True use a sub vocab compute by editions 
                                on source word, the number of editions is n_editions
    """   
    self._matrix_edit_calculator = DynamicEditDistance(insert_w,delete_w)
    if corpus is not None:
      self._vocabulary = Vocabulary(corpus=corpus)
      self._mode = 0
    if tokens is not None:
      self._vocabulary = Vocabulary(collections=tokens)
      self._mode = 1
    
    self._n_suggestions = n_suggestions
    self._n_editions = n_editions
    self._use_sub = use_sub
  def _insert(self,word:str)->list:
    """insert letter process

    Args:
        word (str): word to iterate

    Returns:
        list: list of all possibilities
    """    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return [word[0:i]+letter+word[i:] for i in range(len(word))
            for letter in letters] + [word + letter for letter in letters]
    
  def _delete(self,word:str)->list:
    """delete letter procces 

    Args:
        word (str): word to iterate

    Returns:
        list: list of all possibilities
    """    
    return [word[0:i]+word[i+1:] for i in range(len(word))]
  
  def _replace(self,word:str)->list:
    """replace letter process

    Args:
        word (str): word to iterate

    Returns:
        list: list of all possibilities
    """    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    replace_set = set([word[0:i]+letter+word[i+1:] for i in range(len(word)) 
                       for letter in letters])
    
    replace_list = list(replace_set)
    if word in replace_set:
      index_word = replace_list.index(word)
      replace_list.pop(index_word)
    
    return replace_list
  
  def _edit_one(self,word:str)->set:
    """
      apply the inser, delete and replace process
      generate an list of all possibilitis
    Args:
        word (str): word to edit

    Returns:
        set: set of words edited
    """    
    return set(self._delete(word) + self._replace(word) + self._insert(word))
  
  def _edit_n(self,word:str)->set:
    """apply n editions on word using
    how base the edit_one method

    Args:
        word (str): word to edit

    Returns:
        set: set of all possibilities
    """    
    edits_words = []
    current_words = [word]
    i = 0
    while i < self._n_editions:
      current_editions = []
      for word_select in current_words:
        edit_one_action = self._edit_one(word_select)
        edits_words += edit_one_action
        current_editions+=edit_one_action
      current_words = current_editions
      i += 1
    return edits_words  
  
  def __call__(self, word:str) -> list:
    """for any word in vocabulary compute
    the edit distance from the typed word
    sorted the words for the distance
    and suggest the n_suggestions

    Args:
        word (str): the word typed by the user

    Returns:
        list: list of words and their scores
    """    
    vocab = self._vocabulary
    if self._use_sub:
      vocab = self._edit_n(word)
      vocab = [word for word in tqdm(vocab) if word in self._vocabulary._vocabulary]
      vocab = Vocabulary(collections=vocab)
    n_cores = multiprocessing.cpu_count()
    size_vocab = len(vocab._vocabulary)
    step = int(size_vocab//n_cores)
    results = []
    with ProcessPoolExecutor(max_workers=n_cores) as executor:
      steps =   [[i*step,(i+1)*step] for i in range(n_cores)]
      steps[-1][-1] = steps[-1][-1]+ (size_vocab - n_cores*step)
      for start,end in steps:
        results.append(executor.submit(_apply_edit_distance,
                                      *(self._matrix_edit_calculator,
                                        vocab,word,start,end)))
        
    results = [future.result() for future in tqdm(as_completed(results))]
    items_dict = list(itertools.chain(*(result.items() for result in results)))
    sorted_dists = sorted(items_dict, key= lambda item: item[1])
    min_value = np.array(sorted_dists)[:,1].astype(float).min()
    count_min = np.sum(np.array(sorted_dists)[:,1].astype(float) == min_value)
    
    if count_min >= self._n_suggestions:
      return sorted_dists[:count_min]
    else:
      return sorted_dists[:self._n_suggestions] 
