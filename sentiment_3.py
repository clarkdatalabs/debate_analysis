__author__ = 'kristensheppard'
# -*- coding: utf-8 -*-

import csv
import urllib2
from nltk.parse import stanford

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

# get master of all data from debates from GitHub
url = "https://raw.githubusercontent.com/gtadiparthi/debate-parser/master/all_debates.csv"
webpage = urllib2.urlopen(url)
datareader = csv.reader(webpage.read().splitlines())

from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.analysis import StemmingAnalyzer

import os.path
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin

import codecs
from whoosh.index import create_in, open_dir

from whoosh.query import *


schema = Schema(person=ID(stored=True),
                debate_no=TEXT(stored=True),
                sentiment_score=NUMERIC(stored=True, sortable=True),
                tags=KEYWORD(stored=True),
                category=TEXT(stored=True),
                sentence=TEXT(spelling=True, analyzer=StemmingAnalyzer(), stored=True))

FIELD_KEYWORDS = 'keywords'
FIELD_CONTENT = 'sentences'

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
        row['speaker'] = u'WALKER'
        text = bytearray(row['text'])
        del text[0:7]
        row['text'] = str(text)
        #print row

# for row in transcript:
#     print row

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

# Opening the index back up
ix = open_dir("index")

# creating the testbatch
testbatch=[]
for row in transcript_no_moderators:
    testbatch.append(row)

writer = ix.writer()
sid = SentimentIntensityAnalyzer()
for row in testbatch:
    ss = sid.polarity_scores(row['text'])
    c_score = ss['compound']
    cat = ' '.decode('utf-8')
    if c_score > 0.5:
        cat = 'positive'.decode('utf-8')
    if c_score < 0.5 and c_score > 0.1:
        cat  = 'somewhat positive'.decode('utf-8')
    if c_score > -0.1 and c_score < 0.1:
        cat = 'neutral'.decode('utf-8')
    if c_score > -0.5 and c_score < -0.1:
        cat  = 'somewhat negative'.decode('utf-8')
    if c_score < -0.5:
        cat  = 'negative'.decode('utf-8')
    writer.add_document(person=row['speaker'], debate_no =row['debateNo'], sentence=row['text'], sentiment_score =c_score, category=cat)
writer.commit()


# Here down is that program you run for the actual search. Above should only load once
searcher = ix.searcher()

phrase_to_search = unicode("immigration")

parser = QueryParser("sentence", schema=ix.schema)

q = parser.parse(phrase_to_search)


# this result prints okay
results = searcher.search(q, limit=None)

# print type(results) -- this is a class
# trying to go through results and print the context (i.e. speaker and sentence)
for result in results:
    # print result['person'] + '  ' + result['debate_no'] + ' ' + str(result['sentiment_score'])+  '  ' + result['category'] + '  ' + result['sentence']
    print str(result['sentiment_score'])

# Was this results object created with terms=True?
# if results.has_matched_terms():
        # What terms matched in the results?
    # print(results.matched_terms())


    # What terms matched in each hit?
    # for hit in results:
    #     print(hit.matched_terms())
