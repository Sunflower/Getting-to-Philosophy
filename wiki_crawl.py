import requests
from bs4 import BeautifulSoup as BS
import bs4
import time
import urllib.parse

#start_url = "https://en.wikipedia.org/wiki/Special:Random"
start_url = "https://en.wikipedia.org/wiki/Pikachu"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def continue_crawl(search_history, target_url, max_steps=50):
    if len(search_history) > max_steps:
        print("Search exceeded" + str(max_steps) + "pages")
        return False
    if search_history[-1] == target_url:
        print("Found " + target_url + "!")
        return False
    return True
        
def find_link(article_chain):
    last_page = article_chain[-1]
    
    html = requests.get(last_page).text
    html = BS(html, 'lxml')
    
    found_link = None
    
    wiki_body = html.find(id="mw-content-text").find(class_="mw-parser-output")
    for p in wiki_body.find_all('p', recursive=False):
        inside_parag = p.contents
        in_parenth = False
        for element in inside_parag:
            if type(element) == bs4.element.NavigableString:
                if '(' in element:
                    in_parenth = True
                if ')' in element:
                    in_parenth = False
                continue
            
            if element.name == 'a':
                if in_parenth:
                    continue
                found_link = element.get('href')
                found_link = urllib.parse.urljoin('https://en.wikipedia.org/', found_link)
                if (found_link in article_chain):
                    print("There's a loop! Going to next link!")
                    continue
                return urllib.parse.urljoin('https://en.wikipedia.org/', found_link)

def web_crawl():
    article_chain = [start_url]
    
    while continue_crawl(article_chain, target_url):
        print(article_chain[-1])
        
        found_link = find_link(article_chain)
        if not found_link:
            print("No links found in " + article_chain[-1] + "! Aborting crawl!")
            return
            
        article_chain.append(found_link)
        
        time.sleep(1.5) # use .after() if using tkinter
        
web_crawl()
        
        
