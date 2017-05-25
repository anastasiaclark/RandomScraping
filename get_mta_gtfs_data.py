# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:09:26 2017

@author: AClark
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests,os
import zipfile

mon_year='May2017'

server_path=r'\\DFSN1V-B\Shares\LibShare\Shared\Divisions\Graduate\GEODATA\MASS_Transit'
base_path='http://web.mta.info/developers'

folders_to_create=['nyc_subway','bk_bus','qn_bus','bus_company',
                   'bx_bus','si_bus','mn_bus','LIRR','metro_north','shapes']

for folder in folders_to_create:
    if not os.path.exists(os.path.join(server_path,mon_year,folder)):
        os.makedirs(os.path.join(server_path,mon_year,folder))
        
url='http://web.mta.info/developers/developer-data-terms.html#data'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data,'lxml')
all_links={l.get('href'): l.text for l in soup.find_all('a')}

gtfs=[k for k in all_links.keys() if k is not None and '.zip' in k and k.startswith('data') 
        and 'Shapefiles' not in k and 'Historical' not in k]

gtfs_d={l:all_links[l].strip('-').strip() for l in gtfs}

