import pandas as pd
import time
import random
import logging
logging.disable(logging.INFO)
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import urllib.request
chromedriver = r'./drivers/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
ids = [] 
browser = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
# import match_2text
def get_info_product(link,type_web):
    if (type_web == 'lazada'):
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            img_url = soup.find('div',attrs={'class':'gallery-preview-panel__content'}).img['src'][2:]
        except:
            img_url = ""
        try:
            name_product = soup.find('div',attrs={'class':'pdp-product-title'}).text
        except:
            name_product =""
        try:
            price = soup.find('div',attrs={'class':'pdp-product-price'}).span.text
        except:
            price = ""
    if (type_web=='shopee'):
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            img_url = soup.find('div',attrs={'class':'_2JMB9h _3XaILN'})
            print(img_url)
        except:
            img_url = ""
        try:
            name_product = soup.find('div',attrs={'class':'item-title'}).meta['content']
        except:
            name_product = ""
        try:
            price = soup.find('div',attrs={'class':'price'}).contents[1]['content']
        except:
            price = ""

    if (type_web=='sendo'):
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            name_product = soup.find('h1',attrs={'class':'productName_3Cdc'}).text
        except:
            try:
                name_product = soup.find('div',attrs={'class':'name_product shop_color_hover'}).h1.a.text
            except:
                name_product = ""
        try:
            price = soup.find('strong',attrs={'class':'currentPrice_2zpf'}).text
        except:
            try:
                price = soup.find('div',attrs={'class':'current_price'}).text
            except:
                price = ""
    return {'name':name_product,'price':price,'img_src':img_url}       

def get(link_cat,num_page):
    all_products = []
    link = link_cat.format(num_page)
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    page_product = soup.find_all("script",type='application/ld+json')
    for product in json.loads(page_product[1].contents[0])['itemListElement']:
        p = {}
        p['id'] = product['url'].split('-')[-1].split('.')[0]
        if(p['id'] in ids):
            continue
        ids.append(p['id'])
        p['name'] = product['name']
        p['price'] = product['offers']['price']
        p['img_src'] = product['image']
        p['link_cat'] = link_cat
        urllib.request.urlretrieve(p['img_src'],'./images/'+p['id']+'.jpg')
        p['url'] = product['url']
        all_products.append(p)
    return all_products
links_cat = []
with open('link_cat.txt','r') as lines:
    for line in lines:
        links_cat.append(line.strip()+'?page={}')
print(links_cat)
total_products = []
num_pages = 100
for link_cat in links_cat:
    for i in range(1,num_pages+1):
        print("Page : ",i)
        time.sleep(random.uniform(2, 5))
        while(1):
            try:
                all_products = get(link_cat,i)
                break
            except:
                time.sleep(random.uniform(5, 10))
        total_products.extend(all_products)
        print('products_crawled : ',len(total_products))
with open('data_lazada.json', 'w',encoding='utf-8') as outfile:
    json.dump(total_products,outfile)
browser.close()

