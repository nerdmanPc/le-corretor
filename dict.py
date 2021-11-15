import logging
logging.basicConfig(format = '%(levelname)s: %(message)s', level = logging.DEBUG)

from struct import Struct
from typing import List, Dict

class WordEntry:
    format = Struct('> s30 L s30 L s30 L s30 L')

    def __init__(self, word: str, frequency: int, sequencies: Dict) -> None:
        logging.info(f'Inicializando registro (frequencia: {frequency}, sequencias: {sequencies}).')
        self._word = word
        self._frequency = frequency
        self._sequencies = sequencies

    @classmethod
    def from_str(cls, word: str): # -> Word
        #logging.info(f'Criando registro da palavra "{word}".')
        return cls(word, 0, [])

    @classmethod 
    def from_bytes(cls, data: bytes): #-> Entry
        (word, freq, sq_a, fq_a, sq_b, fq_b, sq_c, fq_c) = cls.format.unpack(data)
        sequencies = {
            sq_a: fq_a,
            sq_b: fq_b,
            sq_c: fq_c
        }
        return WordEntry(word, freq, sequencies)

        logging.info(f'Deserializando registro.')

    def into_bytes(self) -> bytes:
        word = self._word
        freq = self._frequency
        fq_x = []
        sq_x =[]
        for sq, fq in self._sequencies.items():
            sq_x.append(sq)
            fq_x.append(fq)

        data = self.format.pack(\
            word, freq, \
            sq_x[0], fq_x[0], \
            sq_x[1], fq_x[1], \
            sq_x[2], fq_x[2]\
        )

        logging.info(f'Serializando registro.')
        return bytes()

    @classmethod
    def size(cls) -> int:
        logging.info(f'Calculando tamanho do registro.') 
        return cls.format.size

class Dictionary:
    header_format = Struct('> L')
    header_size = header_format.size
    #Esta classe eh similar ao DataBase, mas registra apenas uma vetor
    # de palavras. Cada registro deve conter:
    #   string da palavra
    #   frequencia de digitacao
    #   tres pares referentes ah propostas de sequência, da forma:
    #       (indice, frequencia)
    def __init__(self, dict_path: str) -> None:
        self._dict_path = dict_path
        try:
            with open(dict_path, 'xb') as file:
                self._length = 0
                data = self.header_format.pack(0)
                file.write(data)
        except FileExistsError:
            with open(dict_path,'rb') as file:
                data = file.read(self.header_size)
                (length,) = self.header_format.unpack(data)
                self._length = length

    def count_typing(self, word_index: int):
        logging.info(f'Contou digitacao de "{word_index}"')

    def count_sequence(self, first_index: int, second_index: int):
        logging.info(f'Contou sequencia: "{first_index}" -> "{second_index}"')

    def word_from_index(self, word_index: int) -> str:
        logging.info(f'Consulta string do índice "{word_index}"')

    def add_word(self, word: str) -> int:
        new_entry = WordEntry.from_str(word)
        return self._append_entry(new_entry)

    def __str__(self) -> str:
        return '<Lista de palavras e frequencias>'

    def following_str(self, first_index: int) -> str:
        return '<Lista de palavras e frequencias a partir de "{}">'.format(first_index)

    def empty(self) -> bool:
        return self._length == 0

    @classmethod
    def _index_to_ptr(cls, index: int) -> int:
        entry_size = WordEntry.size()
        header_size = cls.header_size
        #logging.debug(f'Dictionary._index_to_ptr = {header_size} + {index}*{entry_size}')
        return header_size + index * entry_size

    def _set_length(self, length: int) -> None:
        with open(self._dict_path, 'r+b') as file:
            file.seek(0, 0)
            self._length = length
            file.write(self.header_format.pack(length))

    def _append_entry(self, to_append: WordEntry) -> int:
        new_index = self._length
        #logging.debug(f'Dictionary._append_entry(to_append={to_append}): new_index={new_index}')
        self._store_entry(to_append, new_index)
        self._set_length(self._length + 1)
        return new_index

    def _load_entry(self, index: int) -> WordEntry:
        if index >= self._length: print(f'INDICE INVALIDO: {index}')
        load_position = self._index_to_ptr(index)
        with open(self._dict_path, 'rb') as file:
            file.seek(load_position, 0)
            data = file.read(WordEntry.size())
            entry = WordEntry.from_bytes(data)
            return entry

    def _store_entry(self, entry: WordEntry, index: int) -> None:
        if index > self._length: print(f'INDICE INVALIDO: {index}')
        #logging.debug(f'Dictionary._store_entry(entry={entry}, index={index})')
        store_position = self._index_to_ptr(index)
        with open(self._dict_path, 'r+b') as file:
            file.seek(store_position, 0)
            data = entry.into_bytes()
            file.write(data)