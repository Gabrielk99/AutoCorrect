import requests
import os
import yaml
from yaml.loader import SafeLoader
import json
from src.types.vocabulary import Vocabulary

CONST_DIR_YML = os.path.dirname(os.path.realpath(__file__))\
                  .replace("src","conf/parameters.yaml")

def get_url_collection()->str:
  with open(CONST_DIR_YML) as yml:
    conf = yaml.load(yml,Loader=SafeLoader)
    return conf['url_collection']
  
def main():
  response = requests.get(get_url_collection())
  tokens = response.text.split('\n')
  vocabulary = Vocabulary(collections=tokens)
  