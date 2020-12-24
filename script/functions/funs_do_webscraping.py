#importing libraries
import requests  
from bs4 import BeautifulSoup

#pulling webpage
def FindTable(url): 
    page = requests.get(url)
    return page
    return page.status_code

#rendering HTML tags
def GetTags(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    print(soup.prettify())
    return soup

#pulling right wiki table
def GetTable(soup, n):
    wiki_table = soup.find_all('table')[n]
    return wiki_table

#cleaning country names
def replaced(sequence, old, new):
    return (new if x == old else x for x in sequence)