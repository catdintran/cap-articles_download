import csv
import requests
from lxml import html
import string
import os
import pandas as pd

alphabets = string.ascii_lowercase
url = 'http://www.economist.com/economics-a-to-z/'
# User-Agent to fake browser access
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

def scrapEconomist(url):
    page = requests.get(url, headers=header)
    return page.content
    #return html.fromstring(page.content)
    
def get_term_h2(tree):
    return tree.xpath('//div[@class="item-list"]//h2/text()')
def get_defintion_div(tree):
    definition =tree.xpath('//li//div[@class="content clearfix"]//text()')
    defList = []
    i = -1
    for d in definition:
        
        if d in ['\n    ']:
            i += 1
            defList.append('')
        if d not in ['\n  ']:
            defList[i] = defList[i] + d + ' '
    return defList
    

def write_def_to_csv(file, data):
    '''
    Continue to write to csv file w/o overwriting exisitng text
    '''
    try:        
        with open(file, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
    except IOError as err:
        print(err)

    
def read_econ_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)