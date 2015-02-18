from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    pass

@app.route("/inbox")
def inbox():
	pass

@app.route("/analytics")
def analytics():
	pass

if __name__ == "__main__":
    app.run()