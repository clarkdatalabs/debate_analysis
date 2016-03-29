__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import csv
import urllib2

# get master of all data from debates from GitHub
url = "https://raw.githubusercontent.com/gtadiparthi/debate-parser/master/all_debates.csv"
webpage = urllib2.urlopen(url)
datareader = csv.reader(webpage.read().splitlines())

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
    dct['debateNo'] = row[1]
    dct['sentenceNo']=row[2]
    dct['sequenceNo']=row[3]
    dct['speaker']=row[4]
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

rep_speakers = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
dem_speakers = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']

# filtering out moderators
transcript_no_moderators = []
for row in transcript:
    if row['speaker'] in rep_speakers:
        transcript_no_moderators.append(row)
    if row['speaker'] in dem_speakers:
        transcript_no_moderators.append(row)

# list of debate identifiers ('01' for republicans, '1' for democrats)
deb_no = []
for row in transcript:
    deb_no.append(row['debateNo'])
debate_index = sorted(list(set(deb_no)))

# word count for each debate (counts only words spoken by candidates, not by moderators)
def deb_wc(input, party, debateNo):
    count = 0
    for row in input:
        if row['party']== party and row['debateNo'] == debateNo:
            text = row['text'].split()
            #print len(text)
            count += len(text)
    return count

#debate word counts
debate_word_counts = {}
for i in debate_index:
    if deb_wc(transcript_no_moderators, 'rep', i) > 0:
        debate_word_counts['deb_'+ i] = deb_wc(transcript_no_moderators, 'rep', i)
    else:
        continue
for i in debate_index:
    if deb_wc(transcript_no_moderators, 'dem', i) > 0:
        debate_word_counts['deb_'+ i] = deb_wc(transcript_no_moderators, 'dem', i)
    else:
        continue
print debate_word_counts








