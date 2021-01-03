import parsing_functions
from multiprocessing import Pool
from linear_execution import linear_execution
from concurrent_execution import concurrent_execution
from urllib.error import URLError, HTTPError
import urllib.request as urllib
# letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
letter = 'a'
authors, tot_authors_number = parsing_functions.lista_autori_lettera(letter)

if __name__ == '__main__':
    # linear_execution(authors)
    concurrent_execution(authors)
