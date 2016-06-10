# -*- coding: utf-8 -*-
# Got rid of a couple of errors
# One error: can't do dev.app to start the engine and the desktop one (just one or the other)
# Two error: index wasn't importing (it's the index called in search)
# so I moved it into the folder
# turned search.py into a function
# imported the function into main.py in the ResultsHandler
# now trying to get the query to work in the search.py

def function(query):
	import json
	from main import MainHandler
	from whoosh.index import open_dir
	from whoosh.qparser import QueryParser
	import dates

# Opening the index inside of the directory back up coming from sentiment_3
	ix = open_dir("index")

	searcher = ix.searcher()

	phrase_to_search = unicode(query)

	parser = QueryParser("sentence", schema=ix.schema)

	q = parser.parse(phrase_to_search)
# nq = str(q)
# print nq
# token1 = str((nq)).split(':')
# print token1

	results = searcher.search(q, limit=None)

	rep_speakers = ['CRUZ', 'RUBIO', 'KASICH', 'CARSON', 'FIORINA', 'PAUL', 'HUCKABEE', 'WALKER','TRUMP', 'CHRISTIE', 'BUSH']
	dem_speakers = ['CLINTON', 'SANDERS', 'CHAFEE', "O'MALLEY", 'WEBB']

# create list of dictionaries
	lst = []
	for result in results:
		dct = {}
		dct2 = {}
		dct["candidate"] = result['person']
		dct["debate"] = result["debate_no"].lstrip("0")
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

	cat = ["positive", "somewhat positive", "neutral", "somewhat negative", "negative"]
	for i in master:
		for category in cat:
			if category not in i["counts"]:
				i["counts"].update({category: 0})
				i["sentences"].append({"category": category, "text": []})
			else:
				continue

	new_master = {}
	for i in master:
		k = i['candidate' ]+ '_' +i['debate']
		new_master[k] = i

	rep_keys = []
	for i in range(1, 13):
		for rep in rep_speakers:
			rep_keys.append(rep + '_' + str(i))

	dem_keys = []
	for i in range(1, 9):
		for dem in dem_speakers:
			dem_keys.append(dem + '_' + str(i))

	blanks = {'positive': 0, 'neutral': 0, 'somewhat negative': 0, 'negative': 0, 'somewhat positive': 0}

	for i in rep_keys:
		if i not in new_master:
			values = i.split('_')
			new_master[i] = {'counts': blanks, 'debate': values[1], 'candidate': values[0], 'sentences':[]}
			for category in cat:
				new_master[i]["sentences"].append({"category": category, "text": []})

	for i in dem_keys:
		if i not in new_master:
			values = i.split('_')
			new_master[i] = {'counts': blanks, 'debate': values[1], 'candidate': values[0], 'sentences':[]}
			for category in cat:
				new_master[i]["sentences"].append({"category": category, "text": []})

	master2 = []
	for i in new_master:
		master2.append(new_master[i])

	final_lst = []
	for i in master2:
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
		if i['sentences'] == [[]]:
			i['sentences'] = []

	for i in final_lst:
		if i['candidate'] in rep_speakers:
			i['debate_date'] = dates.rep_dates[int(i['debate'])-1]
		elif i['candidate'] in dem_speakers:
			i['debate_date'] = dates.dem_dates[int(i['debate'])-1]

	jstr = {}
	jstr['debate_data'] = final_lst
	json_object = json.dumps(jstr)

	return json_object
