__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import csv
import urllib2

# get master of all data from debates from GitHub
url = "https://raw.githubusercontent.com/gtadiparthi/debate-parser/master/all_debates.csv"
webpage = urllib2.urlopen(url)
datareader = csv.reader(webpage.read().splitlines())

from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.analysis import StemmingAnalyzer

import os.path
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *

schema = Schema(person=ID(stored=True),
                debate_no=TEXT(stored=True),
                sentiment_score=NUMERIC(stored=True),
                sentence=TEXT(analyzer=StemmingAnalyzer()))

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)

# create list of lists
data = []
for row in datareader:
  data.append(row)

# delete header
del data[0]

# create list of dictionaries (using header terms as keys)
transcript = []
for row in data:
    dct = {}
    dct['party'] = row[0]
    dct['debateNo'] = row[1].decode('utf-8')
    dct['sentenceNo']=row[2]
    dct['sequenceNo']=row[3]
    dct['speaker']=row[4].decode('utf-8')
    dct['text']=row[5]
    transcript.append(dct)

# fix error in transcript for second Republican debate (WALKER's lines had been assigned to TRUMP or BUSH)
for row in transcript:
    if row['party'] == 'rep' and row['debateNo']=='02' and row['text'].startswith('WALKER'):
        row['speaker'] = 'WALKER'
        text = bytearray(row['text'])
        del text[0:7]
        row['text'] = str(text)
        #print row

#for row in transcript:
    #print row

# encode sentences as unicode
for row in transcript:
    row['text'] = row['text'].decode('utf-8')

rep_speakers = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
dem_speakers = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']

# filtering out moderators
transcript_no_moderators = []
for row in transcript:
    if row['speaker'] in rep_speakers:
        transcript_no_moderators.append(row)
    if row['speaker'] in dem_speakers:
        transcript_no_moderators.append(row)

ix = open_dir("index")

testbatch=[]
for row in transcript_no_moderators[0:10]:
    testbatch.append(row)

writer = ix.writer()
for row in testbatch:
    writer.add_document(person=row['speaker'], debate_no =row['debateNo'], sentence=row['text'])
writer.commit()

searcher = ix.searcher()

qp = QueryParser("sentence", schema=ix.schema)
q = qp.parse(u"Republican")

with ix.searcher() as searcher:
    results = searcher.search(q)
print results


