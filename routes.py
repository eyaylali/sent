from flask import Flask, render_template, redirect, request, g, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import model
from datetime import datetime

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

@app.route('/sent/api/tickets', methods=['GET'])
def tickets():
	if request.method == 'GET':
		page = int(request.args.get('page'))
		display_qty = 20
	  		
	 	ticket_results = Ticket.query.order_by(model.Ticket.timestamp.desc()).offset((page - 1)*display_qty).limit(display_qty).all()
	  	json_results = []
		for result in ticket_results:
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
		message_count = page + 1
		return jsonify(items=json_results, cursor = message_count)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inbox/<label>", methods=['GET'])
def show_inbox(label):
	return render_template("inbox.html")



# @app.route("/inbox/<int:page>")
# def inbox():
# 	offset = (page-1) * PER_PAGE
# 	user_list = model.session.query(model.User).limit(PER_PAGE).offset(offset)
# 	return render_template("user_list.html", users=user_list, page_num=page)


if __name__ == "__main__":
    app.run(port = 8000, debug = True)