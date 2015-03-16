import os
from flask import Flask, render_template, redirect, request, g, jsonify, url_for, Response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, update, between
import model
from model import session
from datetime import datetime, date, timedelta
import json


app = Flask(__name__)
 
#SERVER ROUTES

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
		last_day = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		#create a list of all hours in a day to query for
		today_by_hour = []
		hour = last_day
		this_hour = today.hour
		for each_hour in range(this_hour):
			hour = hour + timedelta(hours = 1)
			today_by_hour.append(hour)

		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in today_by_hour]
		columns.append(x_axis)
		for label in labels:
			count = {'label':label, 'count':model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp > last_day).count()}
			json_count_results.append(count)
			data_points = [label]

			#line graph data points
			for i in range(len(today_by_hour)):
				if i == (len(today_by_hour) - 1):
					data_point = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp > today_by_hour[i]).count()
					data_points.append(data_point)
				else:
					data_point = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp.between(today_by_hour[i], today_by_hour[i+1])).count()
					data_points.append(data_point)	
			columns.append(data_points)

			#pie graph data
			get_source_data(label, last_day)
		get_source_data("total", last_day)

	if time_period == "week":
		last_week = (today - timedelta(days = 7)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		#create a list of all days of a week to query for
		last_week_by_day = []
		day = last_week
		for each_day in range(7):
			day = day + timedelta(days = 1)
			last_week_by_day.append(day)

		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in last_week_by_day]
		columns.append(x_axis)
		for label in labels:
			count = {'label': label, 'count': model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp > last_week).count()}
			json_count_results.append(count)
			data_points = [label]

			for i in range(7):
				if i == 6:
					data_point = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp > last_week_by_day[i]).count()
					data_points.append(data_point)
				else:
					data_point = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp.between(last_week_by_day[i], last_week_by_day[i+1])).count()
					data_points.append(data_point)	
			columns.append(data_points)

			get_source_data(label, last_week)
		get_source_data("total", last_week)

	if time_period == "month":
		last_month = (today - timedelta(days = 30)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		#create a list of all days of a month to query for
		last_month_by_day = []
		day = last_month
		for each_day in range(30):
			day = day + timedelta(days = 1)
			last_month_by_day.append(day)


		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in last_month_by_day]
		columns.append(x_axis)
		for label in labels:
			count = {'label':label, 'count':model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp > last_month).count()}
			json_count_results.append(count)
			data_points = [label]

			for i in range(30):
				if i == 29:
					data_point = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp > last_month_by_day[i]).count()
					data_points.append(data_point)
				else:
					data_point = model.Ticket.query.filter(model.Ticket.sentiment_label == label, model.Ticket.timestamp.between(last_month_by_day[i], last_month_by_day[i+1])).count()
					data_points.append(data_point)	
			columns.append(data_points)

			get_source_data(label, last_month)
		get_source_data("total", last_month)

	print "SOURCE DATA", source_data

	return jsonify(time_period = time_period, counts=json_count_results, columns = columns, source_data = source_data)


if __name__ == "__main__":
    app.run(port = 10000, debug = True)
