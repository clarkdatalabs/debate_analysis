__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import csv
import urllib2

url = "https://raw.githubusercontent.com/gtadiparthi/debate-parser/master/output/rep_debate1_output.csv"
webpage = urllib2.urlopen(url)
datareader = csv.reader(webpage.read().splitlines())

data = []
for row in datareader:
  data.append(row)

del data[0]

transcript = []

for row in data:
    dct = {}
    key = row[2]
    val = row[3]
    dct[key] = val
    transcript.append(dct)
for row in transcript:
    print row





