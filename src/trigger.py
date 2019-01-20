import script
import selenium
from multiprocessing import Pool

#letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#letters = ['x','y','z']

#letters = ['x']
#letters = ['a','b','c','d','e','f']
#letters = ['g','h','i','j','k','l','m']
#letters = ['n','o','p','q','r','s','t','u','v','w','x','y','z']

letter = 'a'
count = 0

authors , tot_authors_number = script.lista_autori_lettera(letter)
print "Number of authors for letter "+letter+": "+str(tot_authors_number)

if __name__ == '__main__':
    while len(authors)>0:
        authorsToProcess = authors[:20]  

        p = Pool(len(authorsToProcess))
        p.map(script.atomic_operation, authorsToProcess)
        p.close()
        #p.join()


        authors = authors[20:]

        count+=20
        print count

    