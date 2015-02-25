from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn import cross_validation
from sklearn.metrics import classification_report
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from glob import glob
import os
from sys import argv
from tokenizer import tokenize_text
import json

text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])

data = []
target = []

def load_files():
	for filename in glob('test-data/*.json'):
		with open(filename, 'r') as f:
			json_obj = json.load(f)
			for review in json_obj["Reviews"]:
				tokenized, rating = unpack_review(review)
				if rating and tokenized:
					if tokenized not in data:
						target.append(rating)
						data.append(tokenized)
	return data, target

def unpack_review(review):
	if "Title" not in review or "Content" not in review or "Ratings" not in review or "ReviewID" not in review:
		return None, None
	title = review["Title"].encode('ascii','ignore')
	review_content = review["Content"].encode('ascii','ignore')
	author = review["Author"].encode('ascii','ignore')
	id = review["ReviewID"].encode('ascii','ignore')
	rating = review["Ratings"]["Overall"]
	all_content= title +" "+ review_content

	return all_content, rating

def preprocess():
    data,target = load_files()
    vectorizer = CountVectorizer(tokenizer = tokenize_text, lowercase = False)
    data = vectorizer.fit_transform(data)
    tfidf_data = TfidfTransformer(use_idf=False).fit_transform(data)

    return tfidf_data

def learn_model(data,target):
    data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,target,test_size=0.1,random_state=0)
    classifier = BernoulliNB().fit(data_train,target_train)
    predicted = classifier.predict(data_test)
    evaluate_model(target_test,predicted)

# read more about model evaluation metrics here
# http://scikit-learn.org/stable/modules/model_evaluation.html
def evaluate_model(target_true,target_predicted):
    print classification_report(target_true,target_predicted)
    print "The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted))

def main():
	data,target = load_files()
	tf_idf = preprocess()
	learn_model(tf_idf,target)


if __name__ == "__main__":
	main()