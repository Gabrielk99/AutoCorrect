from typing import Any
class SignletonMetaclass(type):
  
  _instance = {}
  
  def __call__(self, *args: Any, **kwds: Any) -> Any:
    
    if self not in self._instance:
      instance = super(SignletonMetaclass,self).__call__(*args, **kwds)
      self._instance[self] = instance
    return self._instance[self]