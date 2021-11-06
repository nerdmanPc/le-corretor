# Terceiro Trabalho Pratico de EDAII (UFBA)
# Desenvolvido em dupla:
# Laila Pereira Mota Santos e Pedro Antonhyonih Silva Costa
# Versão Python 3.8.10

import sys, os
from typing import Optional, Tuple, Union, List
from tests.data_base import DataBase

MAXNSIMBOLOS = 16
FILE_PATH = 'trie.dat'
DICT_PATH = 'dict.dat'


def insert_words(n_words: int):
    data_base = DataBase(FILE_PATH, DICT_PATH)
    #n_words = int(input())
    for i in range(n_words):
        word = input()
        data_base.insert_word(word)

def type_following(first_word: str) -> str:
    data_base = DataBase(FILE_PATH, DICT_PATH)
    following_list = data_base.match_following(first_word)
    following_list = ' '.join(following_list)
    print(f'proximas palavras: {following_list}')
    following_word = input()
    data_base.count_following(first_word, following_word)
    return following_word


def type_word() -> str:
    data_base = DataBase(FILE_PATH, DICT_PATH)
    typed_word = input()
    match_result = data_base.match_word(typed_word)
    print('match_result:', match_result)
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
    
def print_freq_words():
    data_base = DataBase(FILE_PATH, DICT_PATH)
    print(data_base)

def print_freq_after():
    data_base = DataBase(FILE_PATH, DICT_PATH)
    first = input()
    print(data_base.following_str(first))

def exit_shell():
    sys.exit(0)

#Loop principal que processa os comandos
entry = input()
while entry != 'e':
    if(entry == 'i'):
        n_words = int(input())
        insert_words(n_words)
    elif(entry == 'd'):
        type_word()
    elif(entry == 'f'):
        print_freq_words()
    elif(entry == 'p'):
        print_freq_after()
    #print('prox. comando: ', end='')
    entry = input()
exit_shell()