import parsing_functions


def linear_execution(authors):
    count = len(authors)
    for author in authors:
        print("remaining authors: " + str(count))
        parsing_functions.atomic_operation(author)
        count -= 1
