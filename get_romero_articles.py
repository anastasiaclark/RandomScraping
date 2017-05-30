# -*- coding: utf-8 -*-
"""
last modified on: May 29,2017
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
col_names=['authors','year','article','link','journal','issue_volume','pages']

def get_pages(c):
    page=re.search('p\.\s\d+',c)
    pages=re.search(':\d+(-\d+)?',c)
    if page:
        return page.group()
    elif pages:
        return pages.group().replace(':','')
    else:
        return 'None'
    
for e in entries:
    p=get_pages(e.text)
    authors=re.split('\d\d\d\d(\w+)?',e.text)[0].strip() ## splits at 4-digit year, takes first element of the list (should be authors)
    year=re.search('\d\d\d\d(\w+)?',e.text).group()
    if re.search('(\d+)?\(\d+\):\d+(-\d+)?',e.text):
        volume=re.search('(\d+)?\(\d+\):\d+(-\d+)?',e.text).group().strip()
    else:
        volume='None'
        
    if e.a:
        article=e.a.text.replace('\xa0',' ').strip()
        link=e.a.get('href')
    elif e.i:
        article=e.i.text.replace('\xa0',' ').strip()
    elif e.em:
        article=e.em.text.replace('\xa0',' ').strip()
        
    else:
        article='None'
        link='None'
    if e.i:
        journal_parts=[i.text.replace('\xa0',' ') for i in e.findAll('i')]
        journal=' '.join(journal_parts).strip()
    elif e.em:
        journal_parts=[i.text.replace('\xa0',' ') for i in e.findAll('em')]
        journal=' '.join(journal_parts).strip()
    else:
        journal='None'
    row=(authors,year,article,link,journal,volume,p)
    rows.append(row)
    
df=pd.DataFrame(data=rows,columns=col_names) 
df['year']=df.year.str.extract('(?P<digit>\d{4})',expand=False)

splitted=df.authors.str.split('\d\d\d\.')
df['authors']=splitted.apply(lambda x : x[1] if (len(x)>1) else x[0])
        
    
        
    

