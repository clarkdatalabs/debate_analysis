__author__ = 'kristensheppard'

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

# Opening the index inside of the directory back up coming from sentiment_3
ix = open_dir("index")

searcher = ix.searcher()

phrase_to_search = unicode("abortion")

parser = QueryParser("sentence", schema=ix.schema)

q = parser.parse(phrase_to_search)


# this result prints okay
results = searcher.search(q, limit=None)

# print type(results) -- this is a class

# Go through results and print the context
lines_list=[]
for result in results:
    # print result['person'] + '  ' + result['debate_no'] + '  ' + result['sentence']
    person = result['person']
    debate = result['debate_no']
    sentence = result['sentence']
    lines_list = tokenize.sent_tokenize(sentence)
    sentences = lines_list
    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
        # print(sentence)

        # Below here is calculating sentiment and making the integer scores separately
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            sentiment =str('{0}: {1}, '.format(k, ss[k]))
            # print(person + "  " + debate + "  " + sentiment)
            sentiment_split = [sentiment.strip() for x in sentiment.split(",")]

            clean = sentiment_split[1].split(",")
            clean_sentiment= clean[0]
            # print clean_sentiment

            if clean_sentiment.startswith('c'):
                compound_score = str(ss[k])
                c_score = float(compound_score)
            if clean_sentiment.startswith('p'):
                pos_score = str(ss[k])
                p_score = float(pos_score)
            if clean_sentiment.startswith('neu'):
                neu_score = str(ss[k])
                neu_score = float(neu_score)
            if clean_sentiment.startswith('neg'):
                neg_score = str(ss[k])
                neg_score = float(neg_score)

    print(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )


# next steps are to return individual csvs for each query=>
# total number of times     #total positive sentiment       #total neg sentiment