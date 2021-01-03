
from urllib.error import URLError, HTTPError
import urllib.request as urllib

from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import json
import sys
url = 'https://www.brainyquote.com/authors/'


def get_info_author(block):
    info_html = str(block.find_all(
        'div', class_='subnav-below-p')[0])

    info_string = (block.find_all(
        'div', class_='subnav-below-p')[0]).get_text().split('\n')

    info_string_2 = ""

    for element in info_string:
        if(len(element) != 0):
            info_string_2 += element + " "

    return {'info_html': info_html, 'info_string': info_string_2}


def refactor_test_get_quotes_list(author):
    soup = get_soup_page(url+'/authors/'+author)

    quote_list = []
    blocks_list = soup.find_all(
        'div', class_='m-brick grid-item boxy bqQt r-width')

    info_author = get_info_author(soup)

    # bq-subnav-h1

    name_author = " ".join(soup.find_all(
        'h1', class_='bq-subnav-h1')[0].get_text().split()[:-1])

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
    return name_author, info_author, quote_list


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
        '../chromedriver')
    driver.get(page_url)
    driver = scroll_page(driver)
    html = driver.page_source
    driver.close()
    return html


def get_page_with_request(page_url):  # no scrolling but no lag for webdriver
    req = urllib.Request(page_url, headers={'User-Agent': "Magic Browser"})
    con = urllib.urlopen(req)
    return con.read()


def get_page(page_url):
    page = get_page_with_request(page_url)
    return page


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

    for keyword in soup_block.find_all('a', class_='qkw-btn btn btn-xs oncl_klc'):
        keywords.append(keyword.get_text())
    data['keywords'] = keywords
    return data


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
    name, info, quote_list = refactor_test_get_quotes_list(author)
    author_object = {"author": {'name': name, 'url':  author,
                                'info_html': info}, "quotes": quote_list}
    # print(json.dumps(letters, indent=2))
    with open('../authors/'+author+'.json', 'w') as outfile:
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
        # print(json.dumps(letters, indent=2))
        with open('/Users/damianobellucci/Desktop/Projects/scraping-quotes/scraping-quotes1.3.2/'+letter+'.json', 'w') as outfile:
            json.dump(letters, outfile, sort_keys=True, indent=4)
    # test_get_quotes_list(author)

# ok
