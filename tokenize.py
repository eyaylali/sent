import string
import json
import nltk
from nltk.corpus import stopwords
from sys import argv

COMMON_WORDS = ["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"]
NEGATION = ["never","no","nothing","nowhere","noone","none","not","havent","hasnt","hadnt","cant","couldnt","shouldnt","wont","wouldnt","dont","doesnt","didnt","isnt","arent","aint"]
CLAUSE_PUNC =["^","[",".",":",";","!","?","]","$",","]

stopwords = nltk.corpus.stopwords.words('english')
print stopwords
sentence_re = r'''(?x)
		#abbreviations
		([A-Z])(\.[A-Z])+\.?
		#words with optional internal hyphens
		| \w+(-\w+)*
		#currency and percentages
		| \$?\d+(\d+)?%?
		#ellipsis
		| \.\.\.
		#separate tokens
		| [][.,;"'?():-_`]
		'''
all_tokenized_reviews_dict = {}

def unpack(input_file):

	opened_file = open(input_file).read()
	content = json.loads(opened_file)

	for review in content["Reviews"]:
		title = review["Title"].encode('ascii','ignore')
		review_content = review["Content"].encode('ascii','ignore')
		author = review["Author"].encode('ascii','ignore')
		id = review["ReviewID"].encode('ascii','ignore')
		all_text = title + ' ' + review_content

		tokens_all = nltk.regexp_tokenize(all_text, sentence_re)
		tokens_title = nltk.regexp_tokenize(title, sentence_re)
		tokens_content = nltk.regexp_tokenize(review_content, sentence_re)

		print tokens_all

		tokens_all_final = [w for w in tokens_all if w.lower() not in stopwords]
		tokens_title_final = [w for w in tokens_title if w.lower() not in stopwords]
		tokens_content_final = [w for w in tokens_content if w.lower() not in stopwords]
		print tokens_all_final
		tokenized_dict = {"Rating":review["Ratings"]["Overall"], "Title": tokens_title_final, "Author":author, "Content":tokens_content_final, "JoinedContent":tokens_all_final}
		all_tokenized_reviews_dict[id] = tokenized_dict

	# return all_tokenized_reviews_dict
	# print opened_file

# def count(input_list):
# 	words_count = {}
# 	for word in input_list:
# 		if word in IGNORE:
# 			continue
# 		else:

# working_dict[word] = working_dict.get(word, 0) + 1



def main(input_file):
	
	unpacked = unpack(input_file)
	# count1 = count(unpacked[0])
	print unpacked



if __name__ == "__main__":
    script, input_file = argv
    main(input_file)


