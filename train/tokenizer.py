import string
import json
import nltk
from nltk.corpus import stopwords
from sys import argv

COMMON_WORDS = ["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"]
NEGATION = ["never","no","nothing","nowhere","noone","none","not","havent","hasnt","hadnt","cant","couldnt","shouldnt","wont","wouldnt","dont","doesnt","didnt","isnt","arent","aint"]
negation_list = ['never', 'no', 'nothing', 'nowhere', 'noone', 'none', 'not', 'haven\'t', 'havent', 'hasn\'t', 'hasnt', 
                'can\'t', 'cant', 'couldn\'t', 'couldnt', 'shouldn\'t', 'shouldnt', 'won\'t', 'wont', 'wouldn\'t', 'wouldnt', 
                'dont', 'doesnt', 'didnt', 'isnt', 'arent', 'aint', 'don\'t', 'doesn\'t', 'didn\'t', 'isn\'t', 'aren\'t', 'ain\'t']
punctuation_list = ['.', ':', ';', '!', '?']

stopwords = nltk.corpus.stopwords.words('english')

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
		| [.,;"'?():-_`=|/]+
		'''

def tokenize_text(input_string):
		#tokenize with sensitivity towards regular expressions
		tokens = nltk.regexp_tokenize(input_string, sentence_re)
		#remove all stopwords
		tokens_final = [w for w in tokens if w.lower() not in stopwords]
		#preserve words in all caps
		content = [w.lower() if w.isupper() != True else w for w in tokens_final]
		return content

def bag_of_words(list_words):
	return dict([(word, True) for word in list_words])



# if __name__ == "__main__":
#     script, input_file = argv
#     main(input_file)

####TODO####
#remove ' from negation
#preserve emoticons
#think about tweets
#get rid of numbers, $money, 
#add negation

		
