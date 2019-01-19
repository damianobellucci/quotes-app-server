import script
import selenium
from multiprocessing import Pool

#letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#letters = ['x','y','z']

letters = ['x']
#letters = ['a','b','c','d','e','f']
#letters = ['g','h','i','j','k','l','m']
#letters = ['n','o','p','q','r','s','t','u','v','w','x','y','z']

if __name__ == '__main__':
    p = Pool(len(letters))
    print(p.map(script.quote_script, letters))
    #print(p.map(script.test_quote_script, letters))
