# Senti

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Dashboard](#dashboard)
- [Inbox](#inbox)
- [Sentiment Analysis & Machine Learning](#sentiment-analysis-and-machine-learning)
- [ReactJS](#reactjs)
- [Project Structure](#project-structure)

## Introduction

Senti is a tool that helps customer support teams prioritize their ticket queues based on the sentiment of each ticket. When tickets are pulled from Zendesk via the Zendesk API, the content of the message is analyzed with natural language processing and sentiment analysis, categorized using a scikit-learn machine learning algorithm, and ranked in an inbox based on sentiment, source (email vs. social media), and time. Senti also gives teams a visual overview of the sentiment surrounding their company by day, week, and month as well as the capability of drilling down into the ticket source by sentiment for each time period. Since sentiment is subjective and the determinants of it depend on the nature of a business, senti will get smarter when the label is updated in the system with the specific team's feedback!

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

I decided to use the Bernoulli Naive Bayes classifier available with the scikit-learn library. I chose this classifier because the Naive Bayes classifier is a powerful machine learning algorithm that has a demonstrated maintenance of accuracy when applied on text data that is different from the training text data. Since the nature of a business will change determinants of sentiment, I wanted to use a classifier that could be successfully applied to a wider range of data sources. Naive Bayes classifiers also provide good quality for multi-class classification problems like the one I had. Bernoulli Naive Bayes also had the partial fit method available to it, which means that the classifer can be incrementally trained with new information.

Usually, Multinomial Naive Bayes is considered to be the strongest Naive Bayes classifier for text classification, but Bernoulli NB permormed significantly better with my data. It appears that with shorter document length, binarized feature vectors (whether a feature appears or not) is actually more telling than how many times the feature appears. The Bernoulli classifer also penalizes the non-occurence of a feature that is an indicator of a specific label.

Trial and error with different classifiers, vectorizers, tokenizers, and natural language processing activities (running the trained classifier on test data and evaulating with scikit-learn's classification report to compare precision and recall results) led me to Bernoulli Naive Bayes and the final classifer I apply on new Zendesk tickets. However, instead of letting Bernoulli NM decide the label for me, I have it return the probabilities for each label and have a function I wrote determine the final label. I did this in order to improve the recall of negative tickets (low false negatives), since the purpose of my application is to try to catch as many negative tickets as possible. The neutral class was throwing off the results, so I wrote a function that looks to see if the probabilities of neutral and the other classes are close, and if they are, label it the non-neutral label. This improved the recall of the negative class by about .3 and the overall accuracy of the classifer by ~7%.

##ReactJS

React is a good choice when building the UI of applications that have data change over time. My application has a large amount of data flowing through it for both the dashboard and inbox and React makes it easy to fetch data and change the UI accordingly. Instead of re-rendering the the entire DOM, it avoids costly DOM operations by calculating what changes need to be made and updates the DOM tree accordingly (recursively diffs between previous and next renders of a UI). The idea of "components" is also great for organization of the UI, code reuse (I only wrote code for one pie chart, one sentiment counter, one inbox ticket row, etc), testing, and separation of concerns. The data flows are predictable and declared, React manages it all!

##Project Structure


