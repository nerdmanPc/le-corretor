import logging
#logging.basicConfig(format = '%(levelname)s: %(message)s', level = logging.DEBUG)
logging.basicConfig(level = logging.DEBUG)

from typing import List, Dict, Optional
from struct import Struct
from enum import Enum
#Registro de fim de palavra


class ChildType(Enum):
    NONE = 0
    INTERNAL = 1
    WORD = 2

class ChildHandle:
    format = Struct('> B L')

    def __init__(self, type: ChildType, index: int) -> None:
        self._type = type
        self._index = index

    def __str__(self) -> str:
        return '({}, {})'.format(self._type.name, self._index)

    @classmethod
    def new_empty(cls): # -> ChildHandle
        return cls(ChildType.NONE, 0)

    @classmethod
    def new_internal(cls, index: int): # -> ChildHandle
        return cls(ChildType.INTERNAL, index)

    @classmethod
    def new_word(cls, index: int): # -> ChildHandle
        return cls(ChildType.WORD, index)

    def is_empty(self) -> bool: 
        return self._type == ChildType.NONE

    def is_internal(self) -> bool: 
        return self._type == ChildType.INTERNAL

    def is_word(self) -> bool: 
        return self._type == ChildType.WORD

    def index(self) -> Optional[int]:
        if self._type != ChildType.NONE: 
            return self._index
        else:
            return None

    @classmethod 
    def from_bytes(cls, data: bytes): # -> ChildHandle
        #logging.info(f'Deserializando ponteiro para filho.')
        (type, index) = cls.format.unpack(data)
        return ChildHandle( ChildType(type) , index) 

    def into_bytes(self) -> bytes:
        #logging.debug(f'ChildHandle.into_bytes(): self = {self}')
        return self.format.pack(self._type.value, self._index) 

    @classmethod
    def size(cls) -> int:
        return cls.format.size

# LAYOUT NO ARQUIVO [char, ChildHandle, ChildHandle]
class Node:
    header_format = Struct('> c')
    header_size = header_format.size

    def __init__(self, prefix: str, left: ChildHandle, right: ChildHandle) -> None:
        #logging.info(f'Inicializando "node" (letra: {prefix}, filho: {left}, irmao: {right}).')
        self._prefix = prefix
        self._left = left
        self._right = right

    @classmethod
    def from_prefix(cls, prefix: str):
        #logging.info(f'Inicializando node com letra "{prefix}".')
        return cls(prefix, ChildHandle.new_empty(), ChildHandle.new_empty())

    @classmethod 
    def from_bytes(cls, data: bytes): #-> Node
        #logging.info(f'Deserializando node.')
        (prefix,) = cls.header_format.unpack(data[:cls.header_size])
        if prefix != b'\0':
            prefix = str(prefix, 'utf-8')
        else:
            prefix = ''
        left_start = cls.header_size
        right_start = left_start + ChildHandle.size()
        left = ChildHandle.from_bytes(data[left_start:right_start])
        right = ChildHandle.from_bytes(data[right_start:])
        return Node(prefix, left, right)

    def into_bytes(self) -> bytes:
        #logging.info(f'Serializando node.')
        data = bytearray(self.size()) # PREEENCHE COM ZEROS
        if len(self._prefix) == 1:
            prefix_bytes = bytes(self._prefix, 'utf-8')
            data[:self.header_size] = self.header_format.pack(prefix_bytes)
        left_start = self.header_format.size
        right_start = left_start + ChildHandle.size()
        data[left_start:right_start] = ChildHandle.into_bytes(self._left)
        data[right_start:] = ChildHandle.into_bytes(self._right)
        return bytes(data)

    @classmethod
    def size(cls) -> int:
        return cls.header_format.size + 2 * ChildHandle.size()

    def is_prefix(self, word: str) -> bool:
        #logging.info(f'Checa se "{self._prefix}" ?? prefixo de "{word}".')
        if word.startswith(self._prefix):
            return True
        return False

    def take_prefix_from(self, word: str) -> str:
        #logging.info(f'Tira prefixo "{self._prefix}" de "{word}".')
        ptr = self.prefix_size()
        if self.is_prefix(word):
            return word[ptr:]
        return ''

    def prefix_size(self) -> int:
        #logging.info(f'Checa tamanho de "{self._prefix}".')
        return len(self._prefix)
        #return 0

    def set_left(self, new_left: ChildHandle):
        self._left = new_left

    def set_right(self, new_right: ChildHandle):
        self._right = new_right

    def left(self) -> ChildHandle:
        return self._left

    def right(self) -> ChildHandle:
        return self._right