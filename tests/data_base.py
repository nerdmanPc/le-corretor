import logging
logging.basicConfig(level=logging.DEBUG)
from typing import List, Optional, Tuple, Union
from tests.node import Node, Word
from struct import Struct

class DataBase:
    header_format = Struct('> L L')  #Header(length: uint32, root: uint32)
    
    def __init__(self, trie_path: str, dict_path: str):
        self._trie_path = trie_path
        self._dict_path = dict_path
        try:
            with open(trie_path, 'xb') as file:
                logging.info(f'Inicializou arquivo vazio em: "{trie_path}"')
                self._length = 0
                self._root = 0
                file.write(self.header_format.pack(self._length, self._root))
            new_root = self._append_node(Node.new_empty())
            self._set_root(new_root)
        except FileExistsError:
            with open(trie_path, "rb") as file:
                logging.info(f'Abriu arquivo salvo em: "{trie_path}"')
                header = file.read(self._header_size())
                (length, root) = self.header_format.unpack(header)
                self._length = length
                self._root = root
    
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

    @classmethod
    def _header_size(cls) -> int:
        return cls.header_format.size

    @classmethod
    def _index_to_ptr(cls, index: int) -> int:
        node_size = Node.size()
        header_size = cls._header_size()
        return header_size + index * node_size

    def _set_length(self, length: int) -> None:
        with open(self._trie_path, 'r+b') as file:
            file.seek(0, 0)
            self._length = length
            file.write(self.header_format.pack(length, self._root))

    def _set_root(self, root: int) -> None:
        with open(self._trie_path, 'r+b') as file:
            file.seek(0, 0)
            self._root = root
            file.write(self.header_format.pack(self._length, root))

    def _load_node(self, index: int) -> Node:
        if index >= self._length: print(f'INDICE INVALIDO: {index}')
        load_position = self._index_to_ptr(index)
        with open(self._trie_path, 'rb') as file:
            file.seek(load_position, 0)
            data = file.read(Node.size())
            node = Node.from_bytes(data)
            return node

    def _store_node(self, node: Node, index: int) -> None:
        if index > self._length: print(f'INDICE INVALIDO: {index}')
        store_position = self._index_to_ptr(index)
        with open(self._trie_path, 'r+b') as file:
            file.seek(store_position, 0)
            data = node.into_bytes()
            file.write(data)

    def _append_node(self, to_append: Node) -> int:
        new_index = self._length
        self._store_node(to_append, new_index)
        self._set_length(self._length + 1)
        return new_index