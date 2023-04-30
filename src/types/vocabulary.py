import re
from collections import Counter
from dataclasses import dataclass
from unidecode import unidecode
from src.types.singleton import SignletonMetaclass

@dataclass()
class Vocabulary(metaclass=SignletonMetaclass):
  _counter_vocabulary:Counter = None
  _vocabulary:list = None
  def __init__(self,corpus:str=None,collections:list=None) -> None:
    if corpus is not None and self._counter_vocabulary is None:
      corpus = corpus.lower()
      corpus = unidecode(corpus)
      tokens = list(set(re.findall(r'\w+',corpus)))
      self._counter_vocabulary = Counter(tokens)
    if collections is not None and self._vocabulary is None:
      collections = list(set([unidecode(word).lower() for word in collections]))
      self._vocabulary = collections
  