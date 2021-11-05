# Terceiro Trabalho Pratico de EDAII (UFBA)
# Desenvolvido em dupla:
# Laila Pereira Mota Santos e Pedro Antonhyonih Silva Costa
# Versão Python 3.8.10

import sys, os
from typing import Optional, Tuple, Union, List

MAXNSIMBOLOS = 16
FILE_PATH = 'dict.dat'

def insert_words():
    data_base = DataBase(FILE_PATH)
    n_words = int(input())
    for i in range(n_words):
        word = input()
        data_base.insert_word(word)

def type_following(first_word: str) -> str:
    data_base = DataBase(FILE_PATH)
    following_list = data_base.match_following(first_word)
    following_list = ' '.join(following_list)
    print(f'proximas palavras: {following_list}')
    following_word = input()
    data_base.count_following(first_word, following_word)
    return following_word


def type_word() -> str:
    data_base = DataBase(FILE_PATH)
    typed_word = input()
    match_result = data_base.match_word(typed_word)
    # match_result = None, se a palavra esta correta ou match_result = lista de alternativas, se a palavra esta errada
    if match_result is not None:     
        suggestions = ' '.join(match_result)
        print(f'palavra desconhecida - possiveis correcoes: {suggestions}')
        correct_word = input()
        if correct_word == typed_word:
            data_base.insert_word(correct_word)
        data_base.count_word(correct_word)
        return correct_word
    else:
        data_base.count_word(typed_word)
        return typed_word
    

def print_freq_words(): pass

def print_freq_after(): pass

def exit_shell():
    sys.exit(0)
    