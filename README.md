# Senti

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Dashboard](#dashboard)
- [Inbox](#inbox)
- [Sentiment Analysis & Machine Learning](#sentiment-analysis-machine-learning)
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

##Sentiment Analysis & Machine Learning

##ReactJS

##Project Structure

