# Terceiro Trabalho Pratico de EDAII (UFBA)
# Desenvolvido em dupla:
# Laila Pereira Mota Santos e Pedro Antonhyonih Silva Costa
# Versão Python 3.8.10

import logging
import sys, os
from typing import Optional, Tuple, Union, List
from tests.data_base import DataBase

MAXNSIMBOLOS = 16
FILE_PATH = 'trie.dat'
DICT_PATH = 'dict.dat'


def insert_words():
    data_base = DataBase(FILE_PATH, DICT_PATH)
    logging.info('Digite o numero de palavras:')
    n_words = int(input())
    for i in range(n_words):
        logging.info(f'Digite a palavra {i+1}:')
        word = input()
        data_base.insert_word(word)

def type_following(first_word: str) -> str:
    data_base = DataBase(FILE_PATH, DICT_PATH)
    following_list = data_base.match_following(first_word)
    logging.info(f'Resultado da busca de sequencias: {following_list}')
    following_list = ' '.join(following_list)
    print(f'proximas palavras: {following_list}')
    logging.info('Digite a palavra seguinte:')
    following_word = input()
    data_base.count_word(following_word)
    return following_word

# Retorna a palavra contada e se o programa deve sugerir a seguinte
def type_word() -> Tuple[bool, str]:
    data_base = DataBase(FILE_PATH, DICT_PATH)
    logging.info('Digite a palavra desejada:')
    typed_word = input()
    match_result = data_base.match_word(typed_word)
    logging.info(f'Resultado da busca: {match_result}')
    # match_result = None, se a palavra esta correta ou match_result = lista de alternativas, se a palavra esta errada
    if match_result is not None:
        suggestions = ' '.join(match_result)
        print(f'palavra desconhecida - possiveis correcoes: {suggestions}')
        logging.info('Digite a palavra correta:')
        correct_word = input()
        if correct_word == typed_word:
            data_base.insert_word(correct_word)
        data_base.count_word(correct_word)
        return (True, correct_word)
    else:
        data_base.count_word(typed_word)
        return (False, typed_word)
    
def print_freq_words():
    data_base = DataBase(FILE_PATH, DICT_PATH)
    print(data_base)

def print_freq_after():
    data_base = DataBase(FILE_PATH, DICT_PATH)
    logging.info('Digite a palavra a ser consultada:')
    first = input()
    print(data_base.following_str(first))

def exit_shell():
    sys.exit(0)

#Loop principal que processa os comandos
logging.info('Digite o comando:')
entry = input()
while entry != 'e':
    if(entry == 'i'):
        insert_words()
    elif(entry == 'd'):
        (shoud_type_following, correct_first) = type_word()
        if shoud_type_following:
            type_following(correct_first)
    elif(entry == 'f'):
        print_freq_words()
    elif(entry == 'p'):
        print_freq_after()
    #print('prox. comando: ', end='')
    logging.info('Digite o comando:')
    entry = input()
exit_shell()