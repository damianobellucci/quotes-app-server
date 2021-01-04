import parsing_functions
from multiprocessing import Pool
from linear_execution import linear_execution
from concurrent_execution import concurrent_execution
from urllib.error import URLError, HTTPError
import urllib.request as urllib


if __name__ == '__main__':
    letters = ['x', 'z']

    for letter in letters:
        authors = parsing_functions.lista_autori_lettera(letter)
        parsing_functions.dump_authors_letter_list(letter)
        # linear_execution(authors)
        concurrent_execution(authors)
