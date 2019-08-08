import requests
from bs4 import BeautifulSoup
from collections import Counter
import itertools
import string
import csv

categories = [
        'russia', 
        'world', 
        'economics', 
        'forces', 
        'science', 
        'culture', 
        'sport', 
        'media', 
        'travel'
        ]

def get_html(url):
    html_links = {}
    for category in categories:
        url1 = url+'/rubrics/'+category
        print(url1)
        html_page_link = requests.get(url1)
        print('debug2')
        html_page = html_page_link.text
        soup = BeautifulSoup(html_page, 'html.parser')
        print('debug3')
        all_news = soup.find_all('div', class_='item')
        print('debug4')
        links = []
        for new in all_news[0:9]:
            url2 = new.a.get('href')
            links.append(url+url2)
        html_links[category] = links
    return html_links

def get_lenta_news(link):
    html_single_new_page = requests.get(link).text
    soup = BeautifulSoup(html_single_new_page, 'html.parser')
    all_news = soup.find_all('p')
    news_words_list = []
    for new in all_news:
        s = str(new.text).lower()
        a1 = s.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~»«0123456789—""")).split()
        for element in a1:
            news_words_list.append(element)
    return news_words_list

html1 = get_html("https://lenta.ru")

for category, links in html1.items():
    name_file = category+'.csv'
    # print(name_file)
    category_words_list = []
    for link in links:
        words_in_text = get_lenta_news(link)
        category_words_list.extend(words_in_text)
        # print(category_words_list)
    category_words_list_iterabled = list(itertools.chain(category_words_list))
    # print(category_words_list_iterabled)
    counts = Counter(category_words_list)
    counts_20_max = counts.most_common(20)
    # print(category, counts_20_max)
    
    with open(name_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(counts_20_max)


        
        
   