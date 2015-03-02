from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import StratifiedKFold
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
import pandas as pd



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
        label = "neutral"
    else:
        label = "positive"
    return all_content, label

def create_model():
    tfidf = TfidfVectorizer(tokenizer = tokenize_text, lowercase = False, analyzer = "word")
    clf = BernoulliNB()
    pipleline = Pipeline([('vect', tfidf), ('clf', clf)])
    return pipleline

def train_model(clf, review_data, labels):
    cross_validation = StratifiedKFold(labels, n_folds=10, indices=None, shuffle=True, random_state=0)
    review_s = pd.Series(data=review_data)
    labels_s = pd.Series(data=labels)

    for train, test in cross_validation:
        X_train, y_train = review_s[train], labels_s[train]
        X_test, y_test = review_s[test], labels_s[test]

        clf.fit(X_train, y_train)

        predicted = predict(clf, X_test)
        evaluate_model(y_test, predicted)
    joblib.dump(clf, "classifier.pickle")

def predict(clf, test_data):
    results = []
    predict = clf.predict_proba(test_data)
    for label_probability_list in predict:
        neutral = label_probability_list[0]
        positive = label_probability_list[1]
        upset = label_probability_list[2]

        if neutral > positive and neutral > upset:
            if neutral - upset < .20:
                results.append("very upset")
            elif neutral - positive < .20:
                results.append("positive")
            else:
                results.append("neutral")
        else:
            if max(positive, upset) == positive:
                results.append("positive")
            else:
                results.append("very upset")
    results = np.array(results)
    return results


def evaluate_model(label_true,label_predicted):
    print classification_report(label_true,label_predicted)
    print "The accuracy score is {:.2%}".format(accuracy_score(label_true,label_predicted))

def main():
    review_data, labels = parse_files('test/*.json')
    clf = create_model()
    train_model(clf, review_data, labels)

if __name__ == "__main__":
    main()
