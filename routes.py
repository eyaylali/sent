import os
from flask import Flask, render_template, redirect, request, g, jsonify, url_for, Response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, update, between
import model
from model import session
from datetime import datetime, date, timedelta
import json
import pytz


app = Flask(__name__)
 
#PAGE ROUTES

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/inbox/', defaults={'label':'all'})
@app.route('/inbox/<label>')
def show_inbox(label):
	return render_template("inbox.html", label = label)

# API ENDPOINTS

@app.route('/sent/api/tickets/', methods=['POST'])
def update_ticket_sentiment():
	data = request.form
	target_sentiment = data['newSentiment']
	changing_tickets = request.form.getlist('selections[]')

	for ticket_num in changing_tickets:
		session.query(model.Ticket).filter(model.Ticket.ticket_id == ticket_num).update({
			"sentiment_label" : target_sentiment,
			"update_date" : datetime.now()
		})
		session.commit()

	js = json.dumps({"status":"success"})
	
	response = Response(js, mimetype='application/json', status = 200)
	return response

@app.route('/sent/api/tickets/<label>/', methods=['GET'])
def tickets(label):
	if request.method == 'GET':	
		page = int(request.args.get('page'))
		display_qty = 20
		query_qty = 21

		if label == "all":
			 ticket_results = model.Ticket.query.order_by(model.Ticket.priority).order_by(model.Ticket.timestamp.desc()).offset((page - 1)*display_qty).limit(query_qty).all()
		else:
	 		ticket_results = model.Ticket.query.filter(model.Ticket.sentiment_label == label).order_by(model.Ticket.priority).order_by(model.Ticket.timestamp.desc()).offset((page - 1)*display_qty).limit(query_qty).all()
	 	
	 	#to check to see if we will need another paginated page after this page
	 	if len(ticket_results) > 20:
	 		next_page = True
	 	else:
	 		next_page = False

	  	json_results = []
	 	cursor = page
		for result in ticket_results[0:20]:
			# localtz = pytz.timezone('America/Los_Angeles')
			# tz_aware_timestamp = localtz.localize(result.timestamp)
			ticket_day = result.timestamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
			today_day = datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

			if ticket_day == today_day:
				today = True
			else:
				today = False
			d = {
	    		'ticket_id': result.ticket_id,
				'user_id': result.user_id,
				'user_name': result.user.name,
				'user_organization': result.user.organization_name,
				'date': result.timestamp,
				'subject': result.subject,
				'content': result.content,
				'status': result.status,
				'source': result.source,
				'sentiment': result.sentiment_label,
				'today': today
			}
			json_results.append(d)

		all_tickets = model.Ticket.list_all_tickets()

		positive_tickets = []
		upset_tickets = []
		neutral_tickets = []
		total_message_count = []

		for ticket in all_tickets:
			if ticket.sentiment_label == "positive":
				positive_tickets.append(ticket)
			elif ticket.sentiment_label == "upset":
				upset_tickets.append(ticket)
			elif ticket.sentiment_label == "neutral":
				neutral_tickets.append(ticket)

		if label == "positive":
			sentiment_message_count = len(positive_tickets)
		elif label == "upset":
			sentiment_message_count = len(upset_tickets)
		elif label == "neutral":
			sentiment_message_count = len(neutral_tickets)
		else:
			sentiment_message_count = len(positive_tickets) + len(upset_tickets) + len(neutral_tickets)

		total_message_count.append(len(upset_tickets))
		total_message_count.append(len(neutral_tickets))
		total_message_count.append(len(positive_tickets))

		return jsonify(items=json_results, cursor = page, next_page = next_page, total_count = total_message_count, sentiment_count = sentiment_message_count)

@app.route('/sent/api/data/', methods=['GET'])
def counts():

	time_period = request.args.get('time')
	today = datetime.now()
	
	# Query and collect data for each sentiment for the given time range
	json_count_results = []
	columns = []
	source_data = {}
	labels = ["upset", "neutral", "positive", "total"]
	source_options = ["api", "twitter", "facebook"]

	if time_period == "today":
		datetime_threshold = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		#create a list of all hours in a day to query for
		datetime_points = []
		hour = datetime_threshold
		this_hour = today.hour
		for each_hour in range(this_hour):
			hour = hour + timedelta(hours = 1)
			datetime_points.append(hour)

		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in datetime_points]
		columns.append(x_axis)

	if time_period == "week":
		datetime_threshold = (today - timedelta(days = 7)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		#create a list of all days of a week to query for
		datetime_points = []
		day = datetime_threshold
		for each_day in range(7):
			day = day + timedelta(days = 1)
			datetime_points.append(day)

		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in datetime_points]
		columns.append(x_axis)

	if time_period == "month":
		datetime_threshold = (today - timedelta(days = 30)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		#create a list of all days of a month to query for
		datetime_points = []
		day = datetime_threshold
		for each_day in range(30):
			day = day + timedelta(days = 1)
			datetime_points.append(day)

		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in datetime_points]
		columns.append(x_axis)

	#create data points according to timeframe
	all_tickets = model.Ticket.list_tickets(datetime_threshold)
		
	positive_tickets = []
	positive_sources = []
	upset_tickets = []
	upset_sources = []
	neutral_tickets = []
	neutral_sources = []

	for ticket in all_tickets:
		if time_period == "today":
			date_cleaned = ticket.timestamp.replace(minute = 0, second = 0, microsecond = 0)
		else:
			date_cleaned = ticket.timestamp.replace(hour=0, minute = 0, second = 0, microsecond = 0)

		if ticket.sentiment_label == "positive":
			positive_tickets.append(date_cleaned)
			positive_sources.append(ticket.source)
		elif ticket.sentiment_label == "upset":
			upset_tickets.append(date_cleaned)
			upset_sources.append(ticket.source)
		elif ticket.sentiment_label == "neutral":
			neutral_tickets.append(date_cleaned)
			neutral_sources.append(ticket.source)

	#counts by label
	upset_count = {'label':'upset', 'count':len(upset_tickets)}
	json_count_results.append(upset_count)

	neutral_count = {'label':'neutral', 'count':len(neutral_tickets)}
	json_count_results.append(neutral_count)

	pos_count = {'label':'positive', 'count':len(positive_tickets)}
	json_count_results.append(pos_count)

	#initialize data headers
	positive_data_points = ["positive"]
	upset_data_points = ["upset"]
	neutral_data_points = ["neutral"]

	#populate data points
	for date_and_time in datetime_points:
		count = positive_tickets.count(date_and_time)
		positive_data_points.append(count)

	for date_and_time in datetime_points:
		count = upset_tickets.count(date_and_time)
		upset_data_points.append(count)

	for date_and_time in datetime_points:
		count = neutral_tickets.count(date_and_time)
		neutral_data_points.append(count)

	columns.append(upset_data_points)
	columns.append(neutral_data_points)
	columns.append(positive_data_points)

	#function to get ticket source breakdowns for pie charts
	for label in labels:
		all_source_data = []
		for source in source_options:
			if source == "api":
				single_source_data = ["email"]
			else:
				single_source_data = [source]
			if label == "positive":
				single_source_data.append(positive_sources.count(source))
				all_source_data.append(single_source_data)
			elif label == "upset":
				single_source_data.append(upset_sources.count(source))
				all_source_data.append(single_source_data)
			elif label == "neutral":
				single_source_data.append(neutral_sources.count(source))
				all_source_data.append(single_source_data)
			elif label =="total":
				single_source_data.append(positive_sources.count(source) + neutral_sources.count(source) + upset_sources.count(source))
				all_source_data.append(single_source_data)

		source_data[label] = all_source_data
	
	print columns

	return jsonify(time_period = time_period, counts=json_count_results, columns = columns, source_data = source_data)


if __name__ == "__main__":
    app.run(port = 10000, debug = True)
