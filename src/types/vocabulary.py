import re
from collections import Counter
from dataclasses import dataclass
from unidecode import unidecode
from src.types.singleton import SignletonMetaclass

@dataclass(frozen=True)
class Vocabulary(metaclass=SignletonMetaclass):
  _counter_vocabulary:Counter
  
  def __init__(self,corpus:str=None) -> None:
    if corpus is not None:
      corpus = corpus.lower()
      corpus = unidecode(corpus)
      tokens = re.findall(r'\w+',corpus)
      self._counter_vocabulary = Counter(tokens)
    
  