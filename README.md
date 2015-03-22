# Senti

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Dashboard](#dashboard)
- [Inbox](#inbox)
- [Sentiment Analysis & Machine Learning](#sentiment-analysis-and-machine-learning)
- [The Data](#the-data)
- [ReactJS](#reactjs)
- [Project Structure](#project-structure)
- [Next Steps](#project-structure)

## Introduction

Senti is a tool that helps customer support teams prioritize their ticket queues based on the sentiment of each ticket. When tickets are pulled from Zendesk via the Zendesk export API, the content of the message is analyzed with natural language processing and sentiment analysis, assigned a category using a scikit-learn machine learning algorithm, and ranked in an inbox based on sentiment, source (email vs. social media), and time. Senti also gives teams a visual overview of the sentiment surrounding their company by day, week, and month as well as the capability of drilling down into the ticket source by sentiment for each time period. Since sentiment is subjective and the determinants of it depend on the nature of a business, senti will get smarter when the label is updated in the system with the specific team's feedback!

## Technologies

**Backend**

Python, Flask, SQLAlchemy, PostgreSQL, scikit-learn, NLTK, Zendesk API, NumPy, AJAX

**Frontend**

ReactJS, C3.js, Moment.JS, Javascript, HTML, CSS, Bootswatch

## Dashboard

The dashboard of the app allows companies to visualize the sentiment surrounding their business for three time periods, the last 24 hours (for day over day comparisons and real-time updates), last 7 days, and last 30 days. It uses the C3.js library, a D3-based chart library, to display data. The line graph displays the quanity of tickets for each sentiment over time, and the pie charts allow for comparisons of the source of the tickets for total vs. each sentiment. This utility could help teams understand where they are interacting with their customers the most, which sentiment they tend to have over a certain medium, and where to focus their efforts.

The counters provide an up-to-date count of tickets in the inbox for each time period. The counters link through to the corresponding sentiment's inbox.

![dashboard]
(/gifs/graphs.gif)

*Counters and Line Graph*

![dashboard]
(/gifs/piecharts.gif)

*Source pie graphs responding to clicks*

## Inbox

The inbox is organized into multiple inboxes: all tickets, positive, upset, and neutral. Upset emails are highlighted in red and public facing tickets (source from Twitter or Facebook) are tagged with a "public" label. The inbox display is ranked first by urgency of medium and then by date in order for public facing tickets to be prioritized in the inbox. Clicking a ticket will expand to show the content of the ticket, and clicking the blue paper airplane link will link directly into that specific ticket in your Zendesk account to reply!

The most interesting functionality of the inbox is the ability to update the sentiment classification on a ticket. If a customer support representative disagrees with senti's sentiment label, they can update it by clicking on the checkbox and selecting from the dropdown options. This will update the sentiment and update date in the database correspoding to that ticket. Before senti pulls new tickets from Zendesk to classify and display, it will first query the database for any changed sentiment labels based on the update date and feed those tickets to the classifier to incrementally train it with scikit-learn's partial fit method on Naive Bayes classifiers.

![inbox]
(/gifs/inbox.gif)

*Viewing message in inbox, updating sentiment in system, and replying*

##Sentiment Analysis and Machine Learning

I decided to use the Bernoulli Naive Bayes classifier available with the scikit-learn library. I chose this classifier because the Naive Bayes classifier is a powerful machine learning algorithm that has a demonstrated maintenance of accuracy when applied on text data that is different from the training text data. Since the nature of a business will change determinants of sentiment, I wanted to use a classifier that could be successfully applied to a wider range of text sources. Naive Bayes classifiers also provide good quality for multi-class classification problems like the one I had and have the partial fit method available to them, which means that the classifer can be incrementally trained with new information after the initial training.

Usually, Multinomial Naive Bayes is considered to be the strongest Naive Bayes classifier for text classification, but Bernoulli NB permormed significantly better with my data. It appears that with shorter document length, binarized feature vectors (whether a feature appears or not) is actually more telling than how many times the feature appears. The Bernoulli classifer also penalizes the non-occurence of a feature that is an indicator of a specific label.

Instead of using the built-in tokenizer that comes with the feature vectorizer, I wrote my own to allow for greater customization and control over the trial and error process (tokenizer.py). Experimenting with different tokenizing instructions and natural language processing techniques, such as using n-grams to split the text instead of single words, incorporating negation prefixes, preserving emoticons, preserving completely capitalized words, eliminatice noise by removing stopwords and common English words, limiting the feature vocabulary (evaluated by running the trained classifier on test data and evaulating with scikit-learn's classification report to compare precision and recall results for each class), led me to the final vectorizer and trained classifer that I apply on new Zendesk tickets in zendesk_pull.py. However, instead of letting Bernoulli NB decide the label for me, I have it return the probabilities for each label and have a function I wrote determine the final label. I did this in order to improve the recall of negative tickets (catching as many upset emails as possible), since the purpose of my application is to improve response efficiency by urgency of ticket sentiment. The neutral class was throwing off the recall of the upset class, so the function I wrote looks to see if the probability of the neutral class is higher than but close to the probability of another class and labels it the non-neutral label if it is. This improved the recall of the negative class by about .3 and the overall accuracy of the classifer by ~7%.

##The Data

The classifier was trained on a dataset of 200,000+ parsed hotel reviews crawled from [TripAdvisor](http://www.tripadvisor.com). The source of the crawled data can be found [here](http://times.cs.uiuc.edu/~wang296/Data/). Hotel reviews were chosen as the training data because they represent customer sentiment around a service, carry the same self-selection bias as customer support requests, and are labelled with distinct classes (numerical rating). I converted this numerical rating into three groups: 1-2 star reviews were assigned the "upset" label, 3 star reviews were assigned the "neutral" label, and 4-5 star reviews were assigned the "positive" label. Prior to training, the raw data had to be cleaned in order to prevent duplicate reviews and irrelevant/dirty data (missing information such as label, review, author) to affect the classifier.

Before training and testing, I removed a few hundred reviews and created Zendesk tickets with their content. I did this using Zendesk's ticket import API and with the purpose of seeding the Zendesk account I used in order to have tickets to pull into Senti. The script to create these tickets can be found in load_zendesk.py.

The unpacking of the training data, class assignment, feature extraction, training process, and testing process can be found in train.py.

##ReactJS

React is a great choice when building the UI of applications that have data change over time. My application has a large amount of data flowing through it for both the dashboard and inbox and React makes it easy to fetch data and change the UI accordingly. Instead of re-rendering the the entire DOM, it avoids costly DOM operations by calculating what changes need to be made and updates the DOM tree accordingly (recursively diffs between previous and next renders of a UI). The idea of "components" is also great for organization of the UI, code reuse (I only wrote code for one pie chart, one sentiment counter, one inbox ticket row, etc), testing, and separation of concerns. The data flows are predictable and declared, React manages it all!

##Project Structure

**Main application files**

* routes.py: core of the Flask app, lists dashboard and inbox routes, and contains all server API endpoints sending data to client

* zendesk_pull.py: Script that pulls new tickets from Zendesk account, unpacks them to extract information needed for Senti, applies the trained classifier on the raw ticket content to assign a sentiment label to ticket, and commits ticket and user information to database. Before the unpacking process, the database is queried to check if the labels of any tickets already in database have changed (using the update_date column) and the classifier is incrementally trained on this new information.

* model.py: Database class declarations and class methods

* load_zendesk.py: Script to import tickets into Zendesk inbox

**Train directory**

* train.py: The unpacking of the training data, class assignment for training purpose, feature extraction, building the classifier, training process, and testing process

* tokenize.py: In-house tokenizer that extracts relevant features (words that are strong determinants of sentiment) from raw data, used during vectorization in train.py

##Next Steps


