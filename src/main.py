import requests
import os
import yaml
from yaml.loader import SafeLoader
from src.types.vocabulary import Vocabulary
from src.types.auto_correct import AutoCorrect

CONST_DIR_YML = os.path.dirname(os.path.realpath(__file__))\
                  .replace("src","conf/parameters.yaml")

def get_url_collection()->str:
  with open(CONST_DIR_YML) as yml:
    conf = yaml.load(yml,Loader=SafeLoader)
    return conf['url_collection']
 
 
def run(by_tokens:bool):
  #TODO :: implementar versão com corpus
  if by_tokens:
    response = requests.get(get_url_collection())
    tokens = response.text.split('\n')
    autoCorrect = AutoCorrect(tokens=tokens)
  while True:
    word = input("Digite uma palavra palavra para testar o autocorretor:")
    suggestions = autoCorrect(word)
    print(suggestions)
    
def main(by_tokens:bool=True):
  run(by_tokens)
  
if __name__ == "__main__":
  main()