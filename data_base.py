import logging
logging.basicConfig(format = '%(levelname)s: %(message)s', level = logging.DEBUG)

from typing import List, Optional, Tuple, Union
from queue import PriorityQueue
from node import ChildHandle, Node
from dict import Dictionary, WordEntry
from struct import Struct

class DataBase:
    header_format = Struct('> L L l')  #Header(length: uint32, root: uint32)
    
    def __init__(self, trie_path: str, dict_path: str):
        self._trie_path = trie_path
        self._dict = Dictionary(dict_path)
        self._prev_index = -1
        try:
            with open(trie_path, 'xb') as file:
                #logging.info(f'Inicializou arquivo vazio em: "{trie_path}"')
                self._length = 0
                self._root = 0
                #self._prev_index = None
                file.write(self.header_format.pack(self._length, self._root, -1) )
            #new_root = self._append_node(Node.new_empty())
            #self._set_root(new_root)
        except FileExistsError:
            with open(trie_path, "rb") as file:
                #logging.info(f'Abriu arquivo salvo em: "{trie_path}"')
                header = file.read(self._header_size())
                (length, root, prev_index) = self.header_format.unpack(header)
                self._length = length
                self._root = root
                if prev_index >= 0:
                    self._prev_index = prev_index
    
    def insert_word(self, word: str):
        search_result = self._internal_search(word, self._root, 0)
        if len(search_result) > 0:
            return
        word_index = self._dict.add_word(word)
        self._internal_insert(word, word_index, self._root)
        
    def count_word(self, word: str):
        search_result = self._internal_search(word, self._root, 0)[0]
        word_index = search_result.index()
        self._dict.count_typing(word_index)
        if self._prev_index >= 0:
            self._dict.count_sequence(self._prev_index, word_index)
        self._set_prev_index(word_index)
        #logging.info(f'Contou digitacao de "{word}"')

    def match_word(self, word: str) -> Optional[List[str]]:
        #logging.debug(f'Em DataBase.match_word("{word}"):')

        exact_match = self._internal_search(word, self._root, 0)
        if len(exact_match) == 1: #palavra esta correta
            return None

        sorted_queue = PriorityQueue()
        approx_match = self._internal_search(word, self._root, 1)
        #logging.debug(f'approx_match = {approx_match}')

        for word_handle in approx_match:
            word_index = word_handle.index()
            sorted_queue.put(self._dict.word_from_index(word_index))
        #logging.debug(f'sorted_queue = {sorted_queue}')

        result = []
        for i in range(3):
            if sorted_queue.empty():
                break
            next_word = sorted_queue.get()
            result.append(next_word)
        #logging.debug(f'result = {result}')
        return result

    #def count_following(self, first: str, following: str):
    #    logging.info(f'Contou sequencia: "{first}" -> "{following}"')

    def match_following(self, first: str) -> List[str]:
        #logging.info(f'Buscou sequencias a partir de "{first}"')
        #TODO refatorar essa desgraceira
        first_index = self._internal_search(first, self._root, 0)[0]
        entry = self._dict._load_entry(first_index.index())
        #logging.debug(f'Em match_following({first}): palavra={entry.word_str()}\nsequencias=({entry.following_str()})')
        result = []
        for word, freq in entry._sequencies.items():
            result.append(word)
        return result

    def __str__(self) -> str:
        return str(self._dict)

    def following_str(self, first: str) -> str:
        return '<Lista de palavras e frequencias a partir de "{}">'.format(first)

    def _internal_search(self, word: str, node_index: int, distance: int) -> List[ChildHandle]:

        if distance < 0:
            return []
        if self.empty():
            return []
        search_result = []
        node = self._load_node(node_index)
        left_child = node.left()
        right_child = node.right()

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
                search_result.append(left_child)

        if right_child.is_internal():
            right_index = right_child.index()
            next_result = self._internal_search(word, right_index, distance)
            search_result.extend(next_result)
        elif right_child.is_word():
            if word == '':
                search_result.append(right_child)
        return search_result

    def _internal_insert(self, word: str, word_index: int, node_index: int) -> bool: 

        if self.empty():
            new_root = self._new_branch(word, word_index).index()
            self._set_root(new_root)
            return True
        node = self._load_node(node_index)
        left_child = node.left()
        right_child = node.right()

        if node.is_prefix(word):
            after_prefix = node.take_prefix_from(word)
            if left_child.is_internal():
                left_index = left_child.index()
                return self._internal_insert(after_prefix, word_index, left_index)
            elif left_child.is_empty():
                new_left = self._new_branch(after_prefix, word_index)
                node.set_left(new_left)
                self._store_node(node, node_index)
                return True

        if right_child.is_internal():
            right_index = right_child.index()
            return self._internal_insert(word, word_index, right_index)
        elif right_child.is_empty():
            new_right = self._new_branch(word, word_index)
            node.set_right(new_right)
            self._store_node(node, node_index)
            return True
        return False

        
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
            file.write(self.header_format.pack(length, self._root, self._prev_index))

    def _set_prev_index(self, prev_index: int):
        with open(self._trie_path, 'r+b') as file:
            file.seek(0, 0)
            self._prev_index = prev_index
            file.write(self.header_format.pack(self._length, self._root, prev_index))

    def empty(self) -> bool:
        return self._length == 0

    def _set_root(self, root: int) -> None:
        with open(self._trie_path, 'r+b') as file:
            file.seek(0, 0)
            self._root = root
            file.write(self.header_format.pack(self._length, root, self._prev_index))

    def _new_branch(self, after_prefix: str, word_index: int) -> ChildHandle:
        if after_prefix == '':
            new_node = Node.from_prefix('')
            new_node.set_left(ChildHandle.new_word(word_index))
            new_index = self._append_node(new_node)
            return ChildHandle.new_internal(new_index)

        new_node = Node.from_prefix(after_prefix[0])
        new_node.set_left(self._new_branch(after_prefix[1:], word_index))
        new_index = self._append_node(new_node)
        return ChildHandle.new_internal(new_index)

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