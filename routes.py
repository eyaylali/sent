from flask import Flask, render_template, redirect, request, g
import model

app = Flask(__name__)

@app.route("/dashboard")
def index():
    return render_template("index.html")

@app.route("/inbox")
def inbox():
	upset_list = model.session.query(model.Ticket).filter_by(sentiment_label = "positive").all()
	return render_template("inbox.html", upset_list = upset_list)

# @app.route("/inbox/<int:page>")
# def inbox():
# 	offset = (page-1) * PER_PAGE
# 	user_list = model.session.query(model.User).limit(PER_PAGE).offset(offset)
# 	return render_template("user_list.html", users=user_list, page_num=page)

if __name__ == "__main__":
    app.run(port = 8000, debug = True)