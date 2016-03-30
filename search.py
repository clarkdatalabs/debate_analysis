__author__ = 'kristensheppard'

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

# Opening the index inside of the directory back up coming from sentiment_3
ix = open_dir("index")

searcher = ix.searcher()

phrase_to_search = unicode("*")

parser = QueryParser("sentence", schema=ix.schema)

q = parser.parse(phrase_to_search)


# this result prints okay
results = searcher.search(q, limit=None)

# print type(results) -- this is a class

# Go through results and print the context
# lines_list=[]
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
                count = 0

                positive_scores = []
                slightly_positive_scores = []
                neutral = []
                slightly_negative = []
                negative_scores = []

                if c_score > 0.5:
                    positive_scores.append(c_score)
                    # print positive_scores

                if c_score< 0.5 and c_score > 0.1:
                    slightly_positive_scores.append(c_score)
                    # print slightly_positive_scores

                if c_score > -0.1 and c_score < 0.1:
                    neutral.append(c_score)
                    # print neutral

                if c_score > -0.5 and c_score < -0.1:
                    slightly_negative.append(c_score)
                    # print slightly_negative

                if c_score < -0.5:
                    negative_scores.append(c_score)
                    # print negative_scores

            if clean_sentiment.startswith('p'):
                pos_score = str(ss[k])
                p_score = float(pos_score)


            if clean_sentiment.startswith('neu'):
                neu_score = str(ss[k])
                neu_score = float(neu_score)

            if clean_sentiment.startswith('neg'):
                neg_score = str(ss[k])
                neg_score = float(neg_score)

        rep_canidates = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
        dem_candidates = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']

        cruz = rep_canidates[0]
        rubio = rep_canidates[1]
        kasich = rep_canidates[2]
        carson = rep_canidates[3]
        fiorina = rep_canidates[4]
        paul = rep_canidates[5]
        huckabee = rep_canidates[6]
        walker = rep_canidates[7]
        trump = rep_canidates[8]
        christie = rep_canidates[9]
        bush = rep_canidates[10]

        clinton = dem_candidates[0]
        sanders = dem_candidates[1]
        chafee =  dem_candidates[2]
        omalley = dem_candidates[3]
        webb = dem_candidates[4]

        avg = 0
        sum = 0

        if person == cruz:
            cruz_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == rubio:
            rubio_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == kasich:
            kasich_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == carson:
            carson_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == fiorina:
            fiorina_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == paul:
            paul_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == huckabee:
            huckabee_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == walker:
            walker_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == trump:
            trump_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )
            trump_scores = compound_score

        # if debatenumber not in dummydictionary[person]:
        #     dummydictionary[person][debatenumber]=



        if person == christie:
            christie_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )

        if person == bush:
            bush_info = str(person + "  " + debate + "  " + sentence + "  " + "compound: " + str(c_score) + "  " + "positive: " + str(p_score) + "  " + "neutral: " + str(neu_score) + "  " + "negative: " + str(neg_score) )
            # print bush_info

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