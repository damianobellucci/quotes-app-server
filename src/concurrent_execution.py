import parsing_functions
from multiprocessing import Pool


def concurrent_execution(authors):
    remaining_authors = authors
    while len(remaining_authors) > 0:
        print(len(remaining_authors))
        with Pool() as p:
            p.map(parsing_functions.atomic_operation, remaining_authors[:20])
            remaining_authors = remaining_authors[20:]
