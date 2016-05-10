__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import json
import re
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, PhrasePlugin
from whoosh import scoring

# Opening the index inside of the directory back up coming from sentiment_3
ix = open_dir("index")

def raw_scorer(searcher, fieldname, text, matcher):
    poses = matcher.value_as("positions")
    return len(poses)

raw_weighting = scoring.FunctionWeighting(raw_scorer)
searcher = ix.searcher(weighting=raw_weighting)


phrase_to_search = unicode("ISIS")

parser = QueryParser("sentence", schema=ix.schema)
parser.add_plugin(PhrasePlugin)

q = parser.parse(phrase_to_search)

# globally define potential types of output for search phrase
s = ''
s_type = type(s)
l = []
l_type = type(l)

# parse parsed search phrase
nq = str(q)
match = re.search('AND', nq)
if match:
# attempt 2
    # phrase = phrase_to_search.lower()
# attempt 1
#     strip_parentheses = nq[1:-1]
#     words = re.findall(r'[^AND]+',strip_parentheses)
#     print words
#     phrase = ''
#     for word in words:
#         w = word.split(':')
#         phrase += w[1] + ''
#     print phrase
    strip_parentheses = nq[1:-1]
    words = re.findall(r'[^AND]+',strip_parentheses)
    #print words
    phrase = []
    for word in words:
        w = word.strip().split(':')
        phrase.append(w[1])
    #print phrase
else:
    match = re.search(r'^(.*)(:)(.*)', nq)
    phrase = match.group(3)
    #print phrase

results = searcher.search(q, limit=None)

rep_speakers = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
dem_speakers = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']

pos_count = 0
sp_count = 0
neutral_count = 0
sn_count = 0
negative_count = 0
for result in results:
    #print dir(result)
    #print result.score
    #print result['sentiment_score']
    if result['category'] == 'positive':
        pos_count += 1
    if result['category'] == 'somewhat positive':
        sp_count += 1
    if result['category'] == 'neutral':
        neutral_count += 1
    if result['category'] == 'somewhat negative':
        sn_count += 1
    if result['category'] == 'negative':
        negative_count += 1
# print '"Positive" count equals' + ' ' + str(pos_count)
# print '"Somewhat positive" count equals' + ' ' + str(sp_count)
# print '"Neutral" count equals' + ' ' + str(neutral_count)
# print '"Somewhat negative" count equals' + ' ' + str(sn_count)
# print '"Negative" count equals' + ' ' + str(negative_count)
# total = pos_count + sp_count + neutral_count + sn_count + negative_count
# print total
# print len(results)

# create list of dictionaries
lst = []
for result in results:
    dct = {}
    dct2 = {}
    dct["candidate"] = result['person']
    if dct["candidate"] in rep_speakers:
        dct["debate"] = 'R' + result['debate_no']
    else:
        dct["debate"] = 'D'+ result['debate_no']
    dct["sentences"] = dct2
    dct2["text"] = result['sentence'].encode('utf8').decode('ascii','ignore')
    dct2["category"]= result['category']
    dct["join"] = result["person"]+result["debate_no"]
    lst.append(dct)

# create dictionary where 'join' (e.g., FIORINA02) is key
# each value is a list of sentiment categories for that candidate in that debate
to_be_counted = {}
for i in lst:
    to_be_counted[i["join"]] = []
for i in lst:
    if i["join"] in to_be_counted:
        to_be_counted[i["join"]].append(i["sentences"]["category"])

# create new dictionary where occurrences of categories in each list have been counted
counts = {}
for i in to_be_counted:
    l = to_be_counted[i]
    counts_grp = [[x,l.count(x)] for x in set(l)]
    counts[i] = dict(counts_grp)

# insert counts with values in master list of dictionaries
for i in lst:
    key = i["join"]
    if key in counts:
        i["counts"] = counts[key]

# StackOverflow Solution
# source thread : 'Dictionaries inside a List :: Merging Values for the Same Keys'
databykey = {}   # make a new dictionary
for i in lst:    # for each item in the list
    if i["join"] in databykey:
        databykey[i["join"]]["sentences"].append(i["sentences"])
    else:
        databykey[i["join"]]={"candidate": i["candidate"],
                              "debate" : i["debate"],
                              "counts": i["counts"],
                              "sentences": [i["sentences"]]}
# if the item's 'join' key value is already in the dictionary, add its values to the list
# else, add the 'join' key value to the dictionary with the candidate, debate, counts, and the first value

master = []
for i in databykey:
    master.append(databykey[i])

# final_lst = []
# for i in master:
#     final = {}
#     final2 = {}
#     final['candidate'] = i['candidate']
#     for c in i['counts']:
#         #print c , i['counts'][c]
#         final[c] = {}
#         final[c]['debate'] = i['debate']
#         for key in final:
#             if key in i['counts']:
#                 final[c]['count'] = i['counts'][key]
#                 final[c]['sentences'] = []
#
#     final_lst.append(final)

final_lst = []
for i in master:
    for category in i['counts']:
        #print category , i['counts'][category]
        final = {}
        final['candidate'] = i['candidate']
        final['sentiment'] = category
        final['debate'] = i['debate']
        if final['sentiment'] in i['counts']:
            final['count'] = i['counts'][final['sentiment']]
            final['sentences'] = []
            for text in i['sentences']:
                if final['candidate'] == i['candidate'] and final['debate'] == i['debate'] and final['sentiment'] == text['category']:
                    final['sentences'].append(text['text'])
        final_lst.append(final)

for i in final_lst:
    print i






# word counts:
# inaccurate because of punctuation and stemming
# example 'Putin.' will not be counted
# for i in master:
#     sentences = i['sentences']
#     for i in sentences:
#         text = i['text']
#         print text
# attempt one
        # count = 0
        # text = i['text'].split()
        # for word in text:
        #     if word == phrase_to_search:
        #         count +=1
# attempt two
#         p = re.compile(phrase)
#         m = p.findall(text.lower(), re.IGNORECASE)
#         print m
#         i['count'] = len(m)
# attempt three
#         if type(phrase) == s_type:
#             p = re.compile(phrase)
#             m = p.findall(text.lower(), re.IGNORECASE)
#             print m
#             i['count'] = len(m)
#         elif type(phrase) == l_type:
#             for term in phrase:
#                 p = re.compile(term)
#                 m = p.findall(text.lower(), re.IGNORECASE)
#                 print m
#                 print text
#
# for i in master:
#     lst = []
#     sentences = i['sentences']
#     lst = []
#     for sentence in sentences:
#         lst.append(sentence['count'])
#     #print lst
#     i['counts']['total_appearances'] = sum(lst)
    #print i['counts']['total_word_appearances']


jstr = {}
jstr['debate_data'] = final_lst
#print type(jstr)
json_object = json.dumps(jstr)
#print type(json_object)
print json_object
# d = json.loads(json_object)
# print type(d)
# print d

# for i in master:
#     for c in i['sentences']:
#         if c['count'] == 0:
#             print i
