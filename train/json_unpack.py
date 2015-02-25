import string
import json
from glob import glob
import os
from sys import argv
from tokenizer import tokenize_text
import json                          

train_reviews_dict = {}
test_reviews_dict = {}
review_categories = [1,2,3,4,5]

def unpack_review(review):
	if "Title" not in review or "Content" not in review or "Ratings" not in review or "ReviewID" not in review:
		return None, None
	title = tokenize_text(review["Title"].encode('ascii','ignore'))
	review_content = tokenize_text(review["Content"].encode('ascii','ignore'))
	author = review["Author"].encode('ascii','ignore')
	id = review["ReviewID"].encode('ascii','ignore')
	rating = review["Ratings"]["Overall"]
	all_content_tokenized = title + review_content

	tokenized_dict = {"Rating": rating, "Content":all_content_tokenized}
	return id, tokenized_dict

def main():
	counter = 0
	for filename in glob('test-data/*.json'):
		with open(filename, 'r') as f:
			json_obj = json.load(f)
			for review in json_obj["Reviews"]:
				num_train_reviews = int(len(json_obj["Reviews"]) * .9)
				review_id, tokenized = unpack_review(review)
				if review_id and tokenized:
					if tokenized not in train_reviews_dict.values() and tokenized not in test_reviews_dict.values():
						if counter <= num_train_reviews:
							train_reviews_dict[review_id] = tokenized
							counter = counter + 1
						else:
							test_reviews_dict[review_id] = tokenized
		print test_reviews_dict, train_reviews_dict

# if __name__ == "__main__":
#     main()
