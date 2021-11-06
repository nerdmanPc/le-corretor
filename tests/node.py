import logging
logging.basicConfig(level = logging.DEBUG)

from typing import List, Dict, Optional
from struct import Struct
from enum import Enum
#Registro de fim de palavra

class Word:
    format = Struct('')

    def __init__(self, frequency: int, sequencies: List[Dict]) -> None:
        logging.info(f'Inicializando registro (frequencia: {frequency}, sequencias: {sequencies}).')
        self._frequency = frequency
        self._sequencies = sequencies

    @classmethod
    def new_empty(cls): # -> Word
        logging.info(f'Criando registro vazio.')
        return cls(0, [])

    @classmethod 
    def from_bytes(cls, data: bytes): #-> Entry
        logging.info(f'Deserializando registro.')

    def into_bytes(self) -> bytes:
        logging.info(f'Serializando registro.')
        return bytes()

    @classmethod
    def size(cls) -> int:
        logging.info(f'Calculando tamanho do registro.') 
        return 0

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
        return cls(ChildType.NONE, -1)

    @classmethod
    def new_internal(cls, index: int): # -> ChildHandle
        return cls(ChildType.INTERNAL, index)

    @classmethod
    def new_word(cls, index: int): # -> ChildHandle
        return cls(ChildType.WORD, index)

    @classmethod 
    def from_bytes(cls, data: bytes): # -> ChildHandle
        logging.info(f'Deserializando ponteiro para filho.')

    def into_bytes(self) -> bytes:
        logging.info(f'Serializando ponteiro para filho.')

    @classmethod
    def size(cls) -> int:
        return cls.format.size

# LAYOUT NO ARQUIVO [char, ChildHandle, ChildHandle]
class Node:
    header_format = Struct('> c')

    def __init__(self, letter: str, left: ChildHandle, right: ChildHandle) -> None:
        logging.info(f'Inicializando "node" (letra: {letter}, filho: {left}, irmao: {right}).')
        self._letter = letter
        self._left = left
        self._right = right

    @classmethod
    def from_letter(cls, letter: str):
        logging.info(f'Inicializando node com letra "{letter}".')
        return cls(letter, None, None)

    @classmethod 
    def from_bytes(cls, data: bytes): #-> Entry
        logging.info(f'Deserializando node.')

    def into_bytes(self) -> bytes:
        logging.info(f'Serializando node.')

    @classmethod
    def size(cls) -> int:
        return cls.header_format.size + 2*ChildHandle.size()

    def is_prefix(self, word: str) -> bool:
        logging.info(f'Checa se "{self._letter}" é prefixo de "{word}".')
        return False

    def set_left(self, new_left: ChildHandle):
        self._left = new_left

    def set_right(self, new_right: ChildHandle):
        self._right = new_right

    def left(self) -> ChildHandle:
        return self._left

    def right(self) -> ChildHandle:
        return self._right