#from firebase import firebase
import pyrebase
from flask import Flask, render_template, request, session, jsonify, json
#from .forms import FirePut
#from flask_mysqldb import MySQL
from os.path import abspath
import ConfigParser

app = Flask(__name__)

cfg = ConfigParser.ConfigParser()
cfg.read('/home/beauho/Programming/flaskappConfig/config.ini')
#cfg.read('/home/beauho/Programming/flaskappConfig/config.ini')

config = {
  "apiKey": cfg.get('info','FIREBASE_API_KEY'),
  "authDomain": "matchify-7b750.firebaseapp.com",
  "databaseURL": "https://matchify-7b750.firebaseio.com",
  "projectId": "matchify-7b750",
  "storageBucket": "matchify-7b750.appspot.com",
  "serviceAccount": "/home/beauho/Programming/flaskapp/firebase-private-key.json",
  "messagingSenderId": "367663586987"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#app.config['MYSQL_HOST'] = cfg.get('mysqlAccount', 'host')
#app.config['MYSQL_USER'] = cfg.get('mysqlAccount', 'username')
#app.config['MYSQL_PASSWORD'] = cfg.get('mysqlAccount', 'password')
#app.config['MYSQL_DB'] = cfg.get('mysqlAccount', 'database')

#mysql = MySQL(app)

#authentication = firebase.FirebaseAuthentication('arAavmJgKDcBQftCpIuctrJMnVm3S0Azb0c21voB')

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/home")
def template():
	return render_template("home.html")

@app.route("/firebaseTest")
def fbTest():
	new_event = {"Test": "Value"}
	jsonData = json.dumps(new_event)
	db.child("events").push(jsonData)
	#result = firebase.get('/Users', None)
	return str(new_event)

#This page is how to pass key/value pairs to the server side
@app.route("/validate")
def validate():
	username = request.args.get("username")
	password = request.args.get("password")
	return str("username: "+username+" password: "+password)

#This page shows how to export json files
@app.route("/jsontest")
def makejson():
	d = {'car': {'color': 'red', 'make': 'Nissan', 'model': 'Altima'}}
	return jsonify(d)

#This page will be a general controller to the mysql database
#In the future it will have the ability to authenticate accounts
@app.route("/db")
def dbController():
	#Create generalized function based on query arguments
	#Get all arguments
	qString = request.query_string[0:]
	delete = False
	qKeys = ""
	qKeysArr = []
	for char in qString:
		if (char == '='):
			delete = True
		if (char == '&'):
			delete = False
		if (delete == False):
			qKeys += char

	qKeysArr = qKeys.split("&")
	qDict = {}
	for key in qKeysArr:
		qDict[key] = request.args.get(key)

	returnJSON = False
	action = "null"
	if "action" in qDict:
		if (qDict["action"] == "select"):
			returnJSON = True
			action = "select"
		if (qDict["action"] == "proc"):
			returnJSON = True
			action = "proc"
	if ("table" in qDict and qDict["table"].isalpha()):
		table = qDict["table"]
	if ("proc" in qDict and qDict["proc"].isaplpha()):
		proc = qDict["proc"]

	#Make connection with mysql database
	rv = ""
	if (action != "null"):
		cur = mysql.connection.cursor()
		if (action == "select"):
			cur.execute("Select * from "+table)
			rv = cur.fetchall()
		if (action == "proc"):
			cur.execute("call "+proc+"();")
			rv = cur.fetchall()
		#Get header data, and convert result to json
		row_headers=[x[0] for x in cur.description]
		json_data=[]
		for result in rv:
			json_data.append(dict(zip(row_headers,result)))
	#Export data
	if (returnJSON == True):
		return jsonify(json_data)
	else:
		return null

if __name__ == "__main__":
	app.run(debug=True)