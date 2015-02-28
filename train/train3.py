from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.cross_validation import ShuffleSplit, StratifiedKFold, train_test_split
from sklearn.metrics import classification_report
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from glob import glob
import os
from sys import argv
from tokenizer import tokenize_text
import json
from sklearn.externals import joblib
import pdb



text_data = []
labels = []

def parse_files(file_path):
	#iterate through each json file in the data directory, open each file and iterate over reviews. Add review content and ratings to text_data and labels list
	for filename in glob(file_path):
		with open(filename, 'r') as f:
			json_obj = json.load(f)
			for review in json_obj["Reviews"]:
				content, label = unpack_review(review) #retrieve the content and label of the review
				#if a review has content and a rating
				if label and content:
					#if the content of the review isn't a duplicate
					if content not in text_data:
						labels.append(label) #add label of each review ro labels list
						text_data.append(content) #add content of each review (string) to the text_data list
	return text_data, labels

def unpack_review(review):
	if "Title" not in review or "Content" not in review or "Ratings" not in review or "ReviewID" not in review:
		return None, None
	title = review["Title"].encode('ascii','ignore')
	review_content = review["Content"].encode('ascii','ignore')
	author = review["Author"].encode('ascii','ignore')
	id = review["ReviewID"].encode('ascii','ignore')
	rating = review["Ratings"]["Overall"]
	all_content= title +" "+ review_content

	if rating == "1.0" or rating == "2.0":
		label = "very upset"
	elif rating == "3.0":
		label = "dissatisfied"
	else:
		label = "positive"
	return all_content, label

def preprocess(data_list, category_list):
	vectorizer = TfidfVectorizer(tokenizer = tokenize_text, lowercase = False) #Convert a collection of text documents to a matrix of token counts & convert to a matrix of normalized TF-IDF features
	X = vectorizer.fit_transform(data_list) #Learn vocabulary and idf, return term-document matrix
	y = np.array(labels)
	joblib.dump(vectorizer, "vectorizer.pickle")
	return X, y

def learn_model(X,y):
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.1)
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)
    predicted = classifier.predict(X_test)
    evaluate_model(y_test, predicted)
    joblib.dump(classifier, "classifier.pickle")

def evaluate_model(label_true,label_predicted):
    print classification_report(label_true,label_predicted)
    print "The accuracy score is {:.2%}".format(accuracy_score(label_true,label_predicted))

def main():
	review_data, labels = parse_files('test/*.json')
	X, y = preprocess(review_data, labels)
	learn_model(X, y)


if __name__ == "__main__":
	main()