import bs4 as bs
import urllib.request
import pandas as pd
import codecs
import math
import time
import random

#From Bytes URL to string
url_source = 'https://www.imovirtual.com/comprar/terreno/'
url_page =url_source + '?page='
source = urllib.request.urlopen(url_source).read()
soup = bs.BeautifulSoup(source,'lxml')
source_str = codecs.decode(source, 'UTF-8')
chartset_idx_start = source_str.find('charset=')
chartset_idx_end = source_str.find('"', chartset_idx_start, chartset_idx_start+20)
webpage_encoding = source_str[chartset_idx_start+8:chartset_idx_end:1]
source_str2 = codecs.decode(source, webpage_encoding)

#Total ads, todal pages and totals ads last page
tads_idx_start = source_str2.index('totalAds=')
tads_idx_end = source_str2.find('\'',tads_idx_start, tads_idx_start+20)
tads = int(source_str2[tads_idx_start+10:tads_idx_end+6:1])
adds_ppage = 24
tpages = math.ceil(tads/adds_ppage)
adds_lastpage = tads % adds_ppage
print(tads)
print (tpages)
print(adds_lastpage)

#Create dataframe with all webpages with ads
l = ['']
l.clear()
p=1
while p <=tpages:
    if p == 1: l.append(url_source)
    else: l.append(url_page+str(p))
    p += 1
df_webpages = pd.DataFrame(l, columns=['URL'])

#prequisites
sufix = '&search%5Border%5D=filter_float_m%3Adesc'
adpages_dump_list = ['']
adpages_dump_list.clear()

#tpages-1    cod para loop total
i = 1
while i <= tpages-1:
  print(i)
  adpages_list = ['']
  adpages_list.clear()
  #webpages_index = i-1
  #url = df_webpages.iat[webpages_index,0]
  url = df_webpages.iat[i-1,0]
  #if i == 1: url = url_source
  #else: url = url_page+str(i)    
  source = urllib.request.urlopen(url).read()
  soup = bs.BeautifulSoup(source,'lxml')
  for url in soup.find_all('a'):
       urls_str = url.get('href')
       #print(urls_str)
       if urls_str==None or urls_str=="": 
           pass
       adpages_list.append(urls_str)  # Here I modify the last_list, no affectation
  #index1 = adpages_list.index('javascript:void(0)')+7
  #index2 = adpages_list.index(df_webpages.iat[max(0,webpages_index-1),0])
  adpages_dump_list.extend(adpages_list)
  #print(adpages_dump_list)
  #print(len(adpages_dump_list))
  #time.sleep(max(random.gauss(0.11, 0.1),0))
  i += 1
print(adpages_dump_list)