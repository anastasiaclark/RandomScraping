# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests,re,os

url='http://aromerojr.net/wordpress/publications/'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data,'lxml')
entries=soup.findAll(lambda tag:(tag.name=='p' and tag.attrs!={'align': 'center'} or tag.name=='li' and tag.text.startswith('Romero')))
rows=[]
for e in entries:
    words=[i.strip() for i in e.text.replace('\xa0','').split('.')]
    rows.append(words)
    
for row in rows:
    if re.search('\d{3}',rows[0]):
        
    

