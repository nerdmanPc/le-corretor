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
                #logging.info(f'Inicializou arquivo vazio em: "{trie_path}"')
                self._length = 0
                self._root = 0
                file.write(self.header_format.pack(self._length, self._root))
            #new_root = self._append_node(Node.new_empty())
            #self._set_root(new_root)
        except FileExistsError:
            with open(trie_path, "rb") as file:
                #logging.info(f'Abriu arquivo salvo em: "{trie_path}"')
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

    def match_following(self, first: str) -> List[str]:
        logging.info(f'Buscou sequencias a partir de "{first}"')
        return []

    def __str__(self) -> str:
        return '<Lista de palavras e frequencias>'

    def following_str(self, first: str) -> str:
        return '<Lista de palavras e frequencias a partir de "{}">'.format(first)

    def _internal_search(self, word: str, node_index: int, distance: int) -> List[int]:

        if distance < 0:
            return []
        search_result = []
        node = self._load_node(node_index)
        #after_prefix = node.take_prefix(word)
        left_child = node.left()
        right_child = node.right()

        #if node.is_prefix(word):
        if left_child.is_internal():
            left_index = left_child.index()
            if node.is_prefix(word):
                after_prefix = node.take_prefix_from(word)
                next_result = self._internal_search(after_prefix, left_index, distance)
                search_result.extend(next_result)
            else:
                after_prefix = word[node.prefix_size():]
                new_distance = distance - node.prefix_size()
                next_result = self._internal_search(after_prefix, left_index, new_distance)
                search_result.extend(next_result)
        elif left_child.is_word():
            after_prefix = node.take_prefix_from(word)
            if after_prefix == '':
                search_result.append(left_child.index())

        if right_child.is_internal():
            right_index = right_child.index()
            next_result = self._internal_search(word, right_index, distance)
            search_result.extend(next_result)
        elif right_child.is_word():
            if word == '':
                search_result.append(right_child.index())
        
        return search_result
        
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

    def empty(self) -> bool:
        return self._length == 0

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