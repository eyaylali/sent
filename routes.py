from flask import Flask, render_template, redirect, request, g, jsonify, url_for, Response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, update, between
import model
from model import session
from datetime import datetime, date, timedelta
import json


#CONNECTION TO DB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///senti.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
	__tablename__ = "tickets"
	id = db.Column(db.Integer, primary_key = True)
	ticket_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('users.zendesk_user_id'))
	submitter_id = db.Column(db.Integer)
	assignee_id = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)
	subject = db.Column(db.String(200))
	content = db.Column(db.String(3000))
	status = db.Column(db.String(64))
	source = db.Column(db.String(64))
	sentiment_label = db.Column(db.String(64))
	user = db.relationship("User", backref=db.backref("tickets", order_by=id))

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True)
	zendesk_user_id = db.Column(db.Integer)
	role = db.Column(db.String(64))
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	organization_name = db.Column(db.String, nullable = True)

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
		session.query(Ticket).filter(Ticket.ticket_id == ticket_num).update({"sentiment_label" : target_sentiment})
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
			 ticket_results = Ticket.query.order_by(model.Ticket.priority).order_by(model.Ticket.timestamp.desc()).offset((page - 1)*display_qty).limit(query_qty).all()
		else:
	 		ticket_results = Ticket.query.filter(Ticket.sentiment_label == label).order_by(model.Ticket.priority).order_by(model.Ticket.timestamp.desc()).offset((page - 1)*display_qty).limit(query_qty).all()
	 	
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

		sentiment_message_count = Ticket.query.filter(Ticket.sentiment_label == label).count()
		total_message_count = []
		labels = ["upset", "neutral", "positive"]
		for each in labels:
			count = Ticket.query.filter(Ticket.sentiment_label == each).count()
			total_message_count.append(count)

		return jsonify(items=json_results, cursor = page, next_page = next_page, total_count = total_message_count, sentiment_count = sentiment_message_count)

@app.route('/sent/api/data/', methods=['GET'])
def counts():

	time_period = request.args.get('time')
	
	today = datetime.now()
	last_day = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	last_week = (today - timedelta(days = 7)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	last_month = (today - timedelta(days = 30)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)

	#initializing lists to use during querying for graph data points
	today_by_hour = []
	last_week_by_day = []
	last_month_by_day = []

	#create a list of all hours in a day to query for
	hour = last_day
	this_hour = today.hour
	for each_hour in range(this_hour):
		hour = hour + timedelta(hours = 1)
		today_by_hour.append(hour)

	#create a list of all days of a week to query for
	day = last_week
	for each_day in range(7):
		day = day + timedelta(days = 1)
		last_week_by_day.append(day)

	#create a list of all days of a month to query for
	day = last_month
	for each_day in range(30):
		day = day + timedelta(days = 1)
		last_month_by_day.append(day)

	# Query and collect data for each sentiment for the given time_range

	labels = ["upset", "neutral", "positive"]
	json_count_results = []
	columns = []
	source_data = {}
	org_data = []
	source_options = ["api", "twitter", "facebook", "email"]

	#to get all message breakdowns by source

	all_source_data = []
	for source in source_options:
		single_source_data = [source]
		count = Ticket.query.filter(Ticket.source == source).count()
		single_source_data.append(count)
		all_source_data.append(single_source_data)

	source_data["total"] = all_source_data

	if time_period == "today":
		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in today_by_hour]
		columns.append(x_axis)
		for label in labels:
			count = {'label':label, 'count':Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_day).count()}
			json_count_results.append(count)
			data_points = [label]

			#line graph data points
			for i in range(len(today_by_hour)):
				if i == (len(today_by_hour) - 1):
					data_point = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > today_by_hour[i]).count()
					data_points.append(data_point)
				else:
					data_point = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp.between(today_by_hour[i], today_by_hour[i+1])).count()
					data_points.append(data_point)	
			columns.append(data_points)

			all_source_data = []
			for source in source_options:
				single_source_data = [source]
				count = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.source == source, Ticket.timestamp > last_day).count()
				single_source_data.append(count)
				all_source_data.append(single_source_data)

			source_data[label] = all_source_data

	if time_period == "week":
		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in last_week_by_day]
		columns.append(x_axis)
		for label in labels:
			count = {'label': label, 'count': Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_week).count()}
			json_count_results.append(count)
			data_points = [label]

			for i in range(7):
				if i == 6:
					data_point = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_week_by_day[i]).count()
					data_points.append(data_point)
				else:
					data_point = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp.between(last_week_by_day[i], last_week_by_day[i+1])).count()
					data_points.append(data_point)	
			columns.append(data_points)

			all_source_data = []
			for source in source_options:
				single_source_data = [source]
				count = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.source == source, Ticket.timestamp > last_day).count()
				single_source_data.append(count)
				all_source_data.append(single_source_data)

			source_data[label] = all_source_data

	if time_period == "month":
		x_axis = ['x'] + [d.strftime("%Y-%m-%d %H:%M:%S") for d in last_month_by_day]
		columns.append(x_axis)
		for label in labels:
			count = {'label':label, 'count':Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_month).count()}
			json_count_results.append(count)
			data_points = [label]

			for i in range(30):
				if i == 29:
					data_point = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_month_by_day[i]).count()
					data_points.append(data_point)
				else:
					data_point = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp.between(last_month_by_day[i], last_month_by_day[i+1])).count()
					data_points.append(data_point)	
			columns.append(data_points)

			all_source_data = []
			for source in source_options:
				single_source_data = [source]
				count = Ticket.query.filter(Ticket.sentiment_label == label, Ticket.source == source, Ticket.timestamp > last_day).count()
				single_source_data.append(count)
				all_source_data.append(single_source_data)

			source_data[label] = all_source_data
	print source_data

	return jsonify(time_period = time_period, counts=json_count_results, columns = columns, source_data = source_data)


if __name__ == "__main__":
    app.run(port = 10000, debug = True)
