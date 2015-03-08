from flask import Flask, render_template, redirect, request, g, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import model
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sent.db'
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
	url = db.Column(db.String(300))
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

@app.route('/sent/api/tickets/<label>/', methods=['GET'])
def tickets(label):
	if request.method == 'GET':	
		page = int(request.args.get('page'))
		display_qty = 20
		query_qty = 21 

	 	ticket_results = Ticket.query.filter(Ticket.sentiment_label == label).order_by(model.Ticket.priority).order_by(model.Ticket.timestamp.desc()).offset((page - 1)*display_qty).limit(query_qty).all()
	 	
	 	#to check to see if we will need another paginated page after this page
	 	if len(ticket_results) > 20:
	 		next_page = 1
	 	else:
	 		next_page = 0

	  	json_results = []
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
		cursor = page
		total_message_count = []
		Ticket.query.filter(Ticket.sentiment_label == label).count()	
		return jsonify(items=json_results, cursor = page, next_page = next_page, total_count = total_message_count)


@app.route('/sent/api/data/', methods=['GET'])
def counts():

	time_period = request.args.get('time')
	
	today = datetime.now()
	last_day = datetime.now() - timedelta(hours = 24)
	last_week = datetime.now() - timedelta(days = 7)
	last_month = datetime.now() - timedelta(days = 30)
	
	labels = ["upset", "neutral", "positive"]
	json_count_results = []
	if time_period == "today":
		for label in labels:
			count = {'label':label, 'count':Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_day).count()}
			json_count_results.append(count)
	elif time_period == "week":
		for label in labels:
			count = {'label':label, 'count':Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_week).count()}
			json_count_results.append(count)
	elif time_period == "month":
		for label in labels:
			count = {'label':label, 'count':Ticket.query.filter(Ticket.sentiment_label == label, Ticket.timestamp > last_month).count()}
			json_count_results.append(count)

	return jsonify(counts=json_count_results, cursor = time_period)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inbox/<label>")
def show_inbox(label):
	return render_template("inbox.html", label = label)



if __name__ == "__main__":
    app.run(port = 10000, debug = True)