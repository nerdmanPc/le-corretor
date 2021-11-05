import logging
from typing import List, Optional
logging.basicConfig(level=logging.DEBUG)

class DataBase:
    def __init__(self, file_path):
        self._path = file_path
        try:
            with open(file_path, 'xb') as file:
                logging.info(f'Inicializou arquivo vazio em: "{file_path}"')
        except FileExistsError:
            with open(file_path, 'xb') as file:
                logging.info(f'Abriu arquivo salvo em: "{file_path}"')
    
    def insert_word(self, word: str):
        logging.info(f'Inseriu palavra "{word}"')

    def count_word(self, word: str):
        logging.info(f'Contou digitacao de "{word}"')

    def match_word(self, word: str) -> Optional[List[str]]:
        logging.info(f'Buscou palavra "{word}"')
        return None

    def count_following(self, first: str, following: str):
        logging.info(f'Contou sequencia: "{first}" -> "{following}"')

    def match_following(self, first: str):
        logging.info(f'Buscou sequencias a partir de "{first}"')

    def __str__(self) -> str:
        return '<Lista de palavras e frequencias>'

    def following_str(self, first: str) -> str:
        return '<Lista de palavras e frequencias a partir de "{}">'.format(first)