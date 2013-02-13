#!/usr/bin/env python
import re
import urllib2
import csv
from bs4 import BeautifulSoup
import sys
import os

urls = sys.argv[1:]
if len(urls) < 1:
  os._exit(1)

def tableFromTom(url):
  soup = BeautifulSoup(urllib2.urlopen(url).read())
  clLeft = soup.find_all("div","clLeft")[:-1]
  clRight = soup.find_all("div","clRight clearfix")

#Brand series subseries model (codename cores/threads)
  products = map(lambda x:str(x.label.string).strip(), clLeft)

#cpu clock[ (turbo clock)], memory clock, L2[, L3]
  productStats = map(lambda x:str(x.li.span.string).strip(), clLeft)
  
  measurements = map(lambda x:str(x.span.span.string).strip(), clRight)
  summary = zip(products, productStats, measurements)
  benchmark = str(soup.find("h3").string).strip()
  benchmark = re.sub(r'[\[\]]', '', benchmark).replace(' ', '_')
  
  with open('table.' + benchmark, 'w') as tableFile:
    csvTable = csv.writer(tableFile, delimiter='\t', quotechar='"', \
                            quoting=csv.QUOTE_NONNUMERIC)
    csvTable.writerow(('product','product_stats',benchmark))
    csvTable.writerows(summary)
  tableFile.close()

map(tableFromTom, urls)

#http://www.tomshardware.com/charts/cpu-charts-2012/-01-Cinebench-11.5,3142.html
#http://www.tomshardware.com/charts/cpu-charts-2012/-38-System-Peak-Power,3178.html

