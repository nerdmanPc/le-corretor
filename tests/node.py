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
    def __init__(self, type: ChildType, index: int) -> None:
        self._type = type
        self._index = index

    def __str__(self) -> str:
        return '({}, {})'.format(self._type.name, self._index)

class Node:
    def __init__(self, letter: str, first_child: ChildHandle, right_sibling: ChildHandle) -> None:
        logging.info(f'Inicializando "node" (letra: {letter}, filho: {first_child}, irmao: {right_sibling}).')
        self._letter = letter
        self._first_child = first_child
        self._right_sibling = right_sibling

    @classmethod
    def new_empty(cls):
        logging.info(f'Inicializando "node" vazio.')
        return cls('', None, None)