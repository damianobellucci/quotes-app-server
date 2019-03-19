
import urllib2  # for scroll?
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import json
import sys
url = 'https://www.brainyquote.com/authors/'


def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    # scrolling all the page
    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # end scrolling all the page
    return driver


def get_page_with_webdriver(page_url):
    driver = webdriver.Chrome(
        '/Users/damianobellucci/Desktop/Projects/scraping-quotes/scraping-quotes1.3.2/chromedriver')
    driver.get(page_url)
    driver = scroll_page(driver)
    html = driver.page_source
    driver.close()
    return html


def get_page_with_request(page_url):  # no scrolling but no lag for webdriver
    req = urllib2.Request(page_url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    return con.read()


def get_page(page_url):
    return get_page_with_webdriver(page_url)
    # return get_page_with_request(page_url)


def get_soup_page(page):
    soup = BeautifulSoup(get_page(page), 'html.parser')
    return soup

# funzione a supporto di lista_autori_lettera


def get_authors(page):
    author_for_one_page = 0
    soup = get_soup_page(page)
    authors = []
    page_numbers = []

    # find_all mi torna una lista
    for link in soup.find('table', class_="table table-hover table-bordered").find_all('a'):
        # se link ha attributo href e se contiene la stringa /authors/
        if link.get('href') and link.get('href').find('/authors/') != -1:
            # devo lasciare solo il nome dell'autore e togliere il resto
            href_string = link.get('href')
            first_slash = href_string.find('/')
            second_slash = href_string.find('/', first_slash+1)
            href_string = href_string[second_slash+1:]
            authors.append(href_string)
            author_for_one_page = author_for_one_page+1
    return authors, author_for_one_page

# funzione a supporto di lista_autori_letteraaa


def max_index_page(page):
    soup = get_soup_page(page)
    page_numbers = []
    if soup.find('ul', class_='pagination bqNPgn pagination-sm'):
        for link in soup.find('ul', class_='pagination bqNPgn pagination-sm').find_all('a'):
            href_string = link.get('href')
            if href_string and href_string.find('/authors/') != -1:
                href_string = href_string[len('/authors/')+1:]
                page_numbers.append(int(href_string))
        pages = max(page_numbers)
    else:
        pages = 1
    return pages


def get_quote_in_block(data, soup_block):
    data['text'] = soup_block.find_all('a', class_='b-qt')[0].get_text()
    return data


def get_keyword_in_block(data, soup_block):
    keywords = []
    # per ogni citazione prendo le keywords
    for keyword in soup_block.find_all('a', class_='oncl_list_kc'):
        keywords.append(keyword.get_text())
    data['keywords'] = keywords
    return data


def get_bio_in_block_info_author(soup_block_info_author):
    data = {}
    data['name'] = soup_block_info_author.find_all('h1', class_='quoteListH1')[0].get_text()[:-7]

    for el in soup_block_info_author.find_all(href=True):
        data[el['href'].split('/',2)[1]] = el.get_text()
        if el['href'].split('/',2)[1]=='birthdays':
            list_links = soup_block_info_author.find_all('a')
            #print list_links[-1].next_sibling[2:-2]
            data['birthdays'] = data['birthdays']+ ' ' + list_links[-1].next_sibling[2:-2]
            
            data_birthdays_splitted = data['birthdays'].split()
            data['birthdays'] = {'day':data_birthdays_splitted[1],'month':data_birthdays_splitted[0],'year':data_birthdays_splitted[2]}

    return data


def refactor_test_get_quotes_list(author):

    try:
        soup = get_soup_page(url+'/authors/'+author)
    except:
        print 'something wrong '+author
        return []

    quote_list = []
    blocks_list = soup.find_all('div', class_='m-brick grid-item boxy bqQt')

    # gestione blocco info biografia autore
    block_info_author = soup.find_all('div', class_='pull-left bio-under')
    # because block is a BeautifulSoup object, we must stringify it for "re"-soup it
    block_info_author = str(block_info_author)
    soup_block_info_author = BeautifulSoup(block_info_author, 'html.parser')
    info_author = get_bio_in_block_info_author(soup_block_info_author)
    #####

    for block in blocks_list:
        # because block is a BeautifulSoup object, we must stringify it for "re"-soup it
        block = str(block)
        soup_block = BeautifulSoup(block, 'html.parser')
        data = {}

        # take quote, input: data = {} , soup_block . output: data = {'text: 'text of the quote'},'text':'...' appended to data
        data = get_quote_in_block(data, soup_block)
        #####

        # take keywords of quotes input : data, soup_block . output: data = {'keywords':[]} 'keywords':[] appended to data
        data = get_keyword_in_block(data, soup_block)
        #####

        quote_list.append(data)
    return info_author, quote_list


def lista_autori_lettera(letter):
    authors = []
    max_index = max_index_page(url + letter)
    i = 1
    tot_authors_number = 0
    tot_pages = 0
    while i <= max_index:
        part_of_authors, authors_number = get_authors(url+letter+str(i))
        authors = authors + part_of_authors  # concateno liste
        i = i + 1
        tot_pages = tot_pages + 1
        tot_authors_number = tot_authors_number + authors_number
    return authors, tot_authors_number


def atomic_operation(author):
    bio, quote_list = refactor_test_get_quotes_list(author)
    author_object = {"author": {'url': author,
                                'info': bio}, "quotes": quote_list}
    #print(json.dumps(letters, indent=2))
    with open('/Users/damianobellucci/Desktop/Projects/scraping-quotes/scraping-quotes1.3.2/authors/'+author+'.json', 'w') as outfile:
        json.dump(author_object, outfile, sort_keys=True, indent=4)


def test_quote_script(letter):  # with test_get_quotes_list
    letters = {letter: []}
    # authors , tot_authors_number = lista_autori_lettera(letter) #da rimettere dopo fatto testing con un solo autore
    authors = ['aaron_paul']  # only for test
    # print "Number of authors for letter "+letter+": "+str(tot_authors_number) #da rimettere dopo fatto testing con un solo autore
    for author in authors:
        author_object = {"author": {'url': author},
                         "quotes": refactor_test_get_quotes_list(author)}
        letters[letter].append(author_object)
        #print(json.dumps(letters, indent=2))
        with open('/Users/damianobellucci/Desktop/Projects/scraping-quotes/scraping-quotes1.3.2/'+letter+'.json', 'w') as outfile:
            json.dump(letters, outfile, sort_keys=True, indent=4)
    # test_get_quotes_list(author)

# ok
