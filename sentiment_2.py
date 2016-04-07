__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import csv
import urllib2

# get master of all data from debates from GitHub
url = "https://raw.githubusercontent.com/gtadiparthi/debate-parser/master/all_debates.csv"
webpage = urllib2.urlopen(url)
datareader = csv.reader(webpage.read().splitlines())

data = []
for row in datareader:
  data.append(row)

del data[0]

debates = set()
for row in data:
    debates.add(row[1])

print debates
    # dct = {}
    # dct['party'] = row[0]
    # dct['debateNo'] = row[1].decode('utf-8')

# My Work with Whoosh

# from whoosh.fields import Schema, TEXT, ID, NUMERIC
# from whoosh.analysis import StemmingAnalyzer
#
# import os.path
# from whoosh.index import create_in, open_dir
# from whoosh.qparser import QueryParser
# from whoosh.query import *
#
# schema = Schema(person=ID(stored=True),
#                 debate_no=TEXT(stored=True),
#                 sentiment_score=NUMERIC(stored=True),
#                 sentence=TEXT(analyzer=StemmingAnalyzer()))
#
# if not os.path.exists("index"):
#     os.mkdir("index")
# ix = create_in("index", schema)
#
# # create list of lists
# data = []
# for row in datareader:
#   data.append(row)
#
# # delete header
# del data[0]
#
# # create list of dictionaries (using header terms as keys)
# transcript = []
# for row in data:
#     dct = {}
#     dct['party'] = row[0]
#     dct['debateNo'] = row[1].decode('utf-8')
#     dct['sentenceNo']=row[2]
#     dct['sequenceNo']=row[3]
#     dct['speaker']=row[4].decode('utf-8')
#     dct['text']=row[5]
#     transcript.append(dct)
#
# # fix error in transcript for second Republican debate (WALKER's lines had been assigned to TRUMP or BUSH)
# for row in transcript:
#     if row['party'] == 'rep' and row['debateNo']=='02' and row['text'].startswith('WALKER'):
#         row['speaker'] = 'WALKER'
#         text = bytearray(row['text'])
#         del text[0:7]
#         row['text'] = str(text)
#         #print row
#
# #for row in transcript:
#     #print row
#
# # encode sentences as unicode
# for row in transcript:
#     row['text'] = row['text'].decode('utf-8')
#
# rep_speakers = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
# dem_speakers = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']
#
# # filtering out moderators
# transcript_no_moderators = []
# for row in transcript:
#     if row['speaker'] in rep_speakers:
#         transcript_no_moderators.append(row)
#     if row['speaker'] in dem_speakers:
#         transcript_no_moderators.append(row)
#
# ix = open_dir("index")
#
# testbatch=[]
# for row in transcript_no_moderators[0:10]:
#     testbatch.append(row)
#
# writer = ix.writer()
# for row in testbatch:
#     writer.add_document(person=row['speaker'], debate_no =row['debateNo'], sentence=row['text'])
# writer.commit()
#
# searcher = ix.searcher()
#
# qp = QueryParser("sentence", schema=ix.schema)
# q = qp.parse(u"Republican")
#
# with ix.searcher() as searcher:
#     results = searcher.search(q)
# print results

# ********** OLD CODE ********** #
# (FROM search.py) #

# SELWYN'S WORK
# merged_lst = []
# visited_lst = []
#
# for i in range(0, len(lst)):
#     if i in visited_lst:
#         continue
#
#     visited = False
#     new_dict = {}
#     for j in range(i+1, len(lst)):
#         if (lst[i]['debate'] == lst[j]['debate']) and (lst[i]['candidate'] == lst[j]['candidate']):
#             if(not visited):
#                 new_dict['debate'] = lst[i]['debate']
#                 print new_dict['debate']
#                 new_dict['candidate'] = lst[i]['candidate']
#                 print new_dict['candidate']
#                 new_dict['sentences'] = [lst[i]['sentences'], lst[j]['sentences']]
#                 print new_dict['sentences']
#                 # new_dict['counts'] = lst[i]['counts']
#                 visited = True
#                 visited_lst.append(j)
#             else:
#                 new_dict['sentences'].append(lst[j]['sentences'])
#     if (visited):
#         merged_lst.append(new_dict)
#         del new_dict
#     else:
#         merged_lst.append(lst[i])

# for i in merged_lst:
#     if i['candidate'] == 'FIORINA' and i['debate'] == '02':
#         print i

# **** SENTIMENT ANALYSIS CODE, TOKENIZER TO SPLIT BY ACTUAL SENTENCES **** #
    # lines_list = tokenize.sent_tokenize(result['sentence'])
    # sentences = lines_list
    # print sentences
    # sid = SentimentIntensityAnalyzer()
    # for sentence in sentences:
    #     dct = {}
    #     dct2 = {}
    #     dct['candidate'] = result['person']
    #     dct['debate'] = result['debate_no']
    #     dct['sentence'] = dct2
    #     dct2['text'] = sentence.encode('utf8').decode('ascii','ignore')
    #     dct2['category']= result['category']
    #     lst.append(dct)
        #print dct
        # Below here is calculating sentiment and making the integer scores separately
        # ss = sid.polarity_scores(sentence)
        # c_score = ss['compound']
        # if c_score > 0.5:
        #     dct2['category'] = 'positive'
        # if c_score < 0.5 and c_score > 0.1:
        #     dct2['category'] = 'somewhat positive'
        # if c_score > -0.1 and c_score < 0.1:
        #     dct2['category'] = 'neutral'
        # if c_score > -0.5 and c_score < -0.1:
        #     dct2['category'] = 'somewhat negative'
        # if c_score < -0.5:
        #     dct2['category'] = 'negative'

# KRISTEN'S WORK

        # rep_canidates = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
        # dem_candidates = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']
        #
        # cruz = rep_canidates[0]
        # rubio = rep_canidates[1]
        # kasich = rep_canidates[2]
        # carson = rep_canidates[3]
        # fiorina = rep_canidates[4]
        # paul = rep_canidates[5]
        # huckabee = rep_canidates[6]
        # walker = rep_canidates[7]
        # trump = rep_canidates[8]
        # christie = rep_canidates[9]
        # bush = rep_canidates[10]
        #
        # clinton = dem_candidates[0]
        # sanders = dem_candidates[1]
        # chafee =  dem_candidates[2]
        # omalley = dem_candidates[3]
        # webb = dem_candidates[4]
        #
        # if person == cruz:
        #     cruz_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == rubio:
        #     rubio_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == kasich:
        #     kasich_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == carson:
        #     carson_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score+ "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == fiorina:
        #     fiorina_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == paul:
        #     paul_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == huckabee:
        #     huckabee_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == walker:
        #     walker_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == trump:
        #     trump_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #     print trump_info
        # # if debatenumber not in dummydictionary[person]:
        # #     dummydictionary[person][debatenumber]=
        #
        #
        #
        # if person == christie:
        #     christie_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #
        # if person == bush:
        #     bush_info = person + "  " + debate + "  " + sentence.encode('utf8').decode('ascii','ignore') + "  " + "compound: " + compound_score + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score)
        #     # print bush_info

    # print(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )


# next steps are to return individual csvs for each query=>
# total number of times     #total positive sentiment/person       #total neg sentiment/person
# Make a dictionary with columns like 'candidate', 'debate no', 'category', 'count'
# The categories:
#   negative= -1 to -0.5
#   slightly negative = -0.5 to -0.1
#   neutral = -0.1 to 0.1
#   slight positive = 0.1 to 0.5
#   positive = 0.5 to 1
#   we need the count by category and not the averages.. get the count for each of the ones above

# COUNT ACCURACY CHECK
# for i in lst2:
#     if i[0] == "TRUMP12":
#         print i
# for i in counts:
#     if i == "TRUMP12":
#         print i, counts[i]

# DAINA'S OLD EXTRA CODE #
# new data structure for calculating counts of compound scores per candidate by debate
# two-dimensional list
# each list has string made of candidate_name_debate_no and sentence category
# lst2 = []
# for i in lst:
#     lst3 = []
#     lst3.append(i["candidate"] + i["debate"])
#     lst3.append(i["sentences"]["category"])
#     lst2.append(lst3)
# for i in lst2:
#     print i

# merge lists into dictionary
# key is string 'candidate_name_debate_no'
# value is list of all categories, per statement, associated with candidate per debate
# counts = {}
# for i in lst2:
#     counts[i[0]] = []
# for i in lst2:
#     if i[0] in counts:
#         counts[i[0]].append(i[1])


# COUNT ACCURACY CHECK
# for i in lst:
#     if i['candidate'] == 'FIORINA' and i['debate'] == '02':
#         print i
# for i in lst:
#     i["join"] = i["candidate"]+i["debate"]