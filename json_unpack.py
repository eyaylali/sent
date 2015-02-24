import string
import json
from glob import glob
import os
from sys import argv
from tokenizer import tokenize_text               # import numpy
import json                          # library for reading json in python


all_tokenized_reviews_dict = {}

def unpack(json_obj):
	for review in json_obj["Reviews"]:
		if "Title" not in review or "Content" not in review or "Ratings" not in review:
			continue
		title = tokenize_text(review["Title"].encode('ascii','ignore'))
		review_content = tokenize_text(review["Content"].encode('ascii','ignore'))
		author = review["Author"].encode('ascii','ignore')
		id = review["ReviewID"].encode('ascii','ignore')
		rating = review["Ratings"]["Overall"]
		all_content_tokenized = title + review_content

		tokenized_dict = {"Rating": rating, "Content":all_content_tokenized}
		# if tokenized_dict in all_tokenized_reviews_dict.values():
		# 	continue
		all_tokenized_reviews_dict[tokenized_dict] = id
	return all_tokenized_reviews_dict

def main():
	count = 0
	for filename in glob('data/*.json'):
		print filename
		with open(filename, 'r') as f:
			json_obj = json.load(f)
			tokenized = unpack(json_obj)
			#assign 90% to training set and 10% to testing set
			count = count +1
			print tokenized, count

if __name__ == "__main__":
    # script, input_path= argv
    main()
