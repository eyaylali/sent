import string
import json
from glob import glob
import os
from sys import argv
from tokenizer import tokenize_text
import pandas as pd                  # import pandas library
import numpy as np                   # import numpy
import json                          # library for reading json in python
import urllib                        # need this for reading urls
import matplotlib.pyplot as plt

all_tokenized_reviews_dict = {}

def unpack(input_file):
	for review in content["Reviews"]:
		title = tokenize_text(review["Title"].encode('ascii','ignore'))
		review_content = tokenize_text(review["Content"].encode('ascii','ignore'))
		author = review["Author"].encode('ascii','ignore')
		id = review["ReviewID"].encode('ascii','ignore')
		rating = review["Ratings"]["Overall"]
		all_content_tokenized = title + review_content

		tokenized_dict = {"Rating": rating, "Content":all_tokenized_content}
		all_tokenized_reviews_dict[id] = tokenized_dict
	return json.dumps(all_tokenized_reviews_dict)

def main():
	for filename in glob('~/data/*.json'):
		with open(filename, 'r') as f:
			content = json.loads(f)
			tokenized = unpack(content)
			#assign 90% to training set and 10% to testing set
			print tokenized

if __name__ == "__main__":
    # script, input_path= argv
    main()
