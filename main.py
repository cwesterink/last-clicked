from flask import Flask, flash, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy #this is the database to store that most recent click
app = Flask(__name__) #creates the flask app
from datetime import *

db = SQLAlchemy()

class ClickTime(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    time= db.Column(db.String())

app.config['SECRET_KEY'] = 'keppThis secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #this sets the name of the database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) #connect the db to the flask app




db.create_all(app=app) #<--run this code once to create the database file
#when created you can block this code out

@app.route("/", methods=["POST", "GET"])
def index():
    lastedClick = ClickTime.query.first() #this will get the last time the button has been click in the db if there is nothing in db it will return None
    try:
        lastedClick = lastedClick.time #This will get the time
    except:
        lastedClick = "Has not yet been clicked" # if nothing exists this will show up

    return render_template("index.html", clickTime = lastedClick) #renders the html page with clicktime as a variable


@app.route("/click", methods=["POST", "GET"])
def click():
    #this code below gets the current time
    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    year = str(datetime.now().year)
    month = months[datetime.now().month-1]
    day = str(datetime.now().day)
    hour = str(datetime.now().hour)
    min = str(datetime.now().minute)
    sec = str(datetime.now().second)

    time = f"{hour}:{min} {sec}secs"

    timeInString = f"{month} {day}, {year} at {time}"
    #timeInString will look like this:
    #may 13, 2021 at 11:32 34secs
    if ClickTime.query.count() == 0: #if nothing is in database
        newClick = ClickTime(time=timeInString) #it will add clicktime to database with time
        db.session.add(newClick)

    else:
        editClick = ClickTime.query.first() #if something in database
        editClick.time = timeInString #it will edit time of the intance

    db.session.commit() #commit new changed to db
    #note: at all time there will at most be one row in databse


    return redirect(url_for("index")) #redirects to the "index" function

app.run() #runs the app