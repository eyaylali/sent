import os
from flask import Flask, render_template, redirect, request, g, jsonify, url_for, Response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, update, between
import model
from model import session
from datetime import datetime, date, timedelta
import json


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
				'sentiment': result.sentiment_label
			}
			json_results.append(d)

		sentiment_message_count = model.Ticket.query.filter(model.Ticket.sentiment_label == label).count()
		total_message_count = []
		labels = ["upset", "neutral", "positive"]
		for each in labels:
			count = model.Ticket.query.filter(model.Ticket.sentiment_label == each).count()
			total_message_count.append(count)

		return jsonify(items=json_results, cursor = page, next_page = next_page, total_count = total_message_count, sentiment_count = sentiment_message_count)

@app.route('/sent/api/data/', methods=['GET'])
def counts():

	time_period = request.args.get('time')
	today = datetime.now()
	
	# Query and collect data for each sentiment for the given time range
	json_count_results = []
	columns = []
	source_data = {}
	labels = ["upset", "neutral", "positive"]
	source_options = ["api", "twitter", "facebook"]
	
	#function to get ticket source breakdowns
	def get_source_data(label, time_param):
		all_source_data = []
		for source in source_options:
			if source == "api":
				single_source_data = ["email"]
			else:
				single_source_data = [source]

			if label == "total":
				count = model.Ticket.query.filter(model.Ticket.source == source, model.Ticket.timestamp > time_param).count()
			else:
				count = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.source == source, model.Ticket.timestamp > time_param).count()
			
			single_source_data.append(count)
			all_source_data.append(single_source_data)

		source_data[label] = all_source_data

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
		
	#pie graph data
	get_source_data("total", datetime_threshold)
	
	#pie graph data by sentiment
	for label in labels:
		get_source_data(label, datetime_threshold)
		
	positive_tickets = []
	upset_tickets = []
	neutral_tickets = []

	for ticket in all_tickets:
		if ticket.sentiment_label == "positive":
			positive_tickets.append(ticket.timestamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0))
		elif ticket.sentiment_label == "upset":
			upset_tickets.append(ticket.timestamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0))
		elif ticket.sentiment_label == "neutral":
			neutral_tickets.append(ticket.timestamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0))

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

	print "UPSET TICKETS", upset_tickets

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

	columns.append(positive_data_points)
	columns.append(upset_data_points)
	columns.append(neutral_data_points)


	print "SOURCE DATA", source_data
	print columns

	return jsonify(time_period = time_period, counts=json_count_results, columns = columns, source_data = source_data)


if __name__ == "__main__":
    app.run(port = 10000, debug = True)
