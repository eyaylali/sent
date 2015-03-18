# Senti

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Dashboard](#dashboard)
- [Inbox](#inbox)
- [Sentiment Analysis](#sentiment-analysis)
- [Machine Learning](#machine-learning)
- [ReactJS](#reactjs)
- [Installation](#installation)

## Introduction

Senti is a tool that helps customer support teams prioritize their ticket queues based on the sentiment of each ticket. When tickets are pulled from Zendesk via the Zendesk API, the content of the message is analyzed with natural language processing and sentiment analysis, categorized using a scikit-learn machine learning algorithm, and ranked in an inbox based on sentiment, source (email vs. social media), and time. Senti also gives teams a visual overview of the sentiment surrounding their company by day, week, and month as well as the capability of drilling down into the ticket source by sentiment for each time period. Since sentiment is subjective and the determinants of it depend on the nature of a business, senti will get smarter when the label is updated in the system with the specific team's feedback!

## Technologies

**Backend**

Python, Flask, SQLAlchemy, PostgreSQL, scikit-learn, NLTK, Zendesk API, NumPy, AJAX

**Frontend**

ReactJS, C3.js, Javascript, HTML, CSS, Bootswatch

## Dashboard

![dashboard]
(/gifs/graphs.gif)

*Counters and Line Graph*

![dashboard]
(/gifs/piecharts.gif)

*Source pie graphs responding to clicks*

![inbox]
(/gifs/inbox.gif)

*Viewing message in inbox, updating sentiment in system, and relpying*

