from flask import Flask, render_template, redirect, request, g
import model

app = Flask(__name__)

@app.before_request
def before_request():
	g.user_list = model.session.query(model.User).all()
	g.unread_message_list = model.session.query(model.Ticket).all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inbox")
def inbox():
	pass

@app.route("/analytics")
def analytics():
	pass

if __name__ == "__main__":
    app.run(debug = True)