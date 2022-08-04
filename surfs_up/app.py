#Import dependencies
import datetime as dt
from secrets import token_bytes
from turtle import end_fill 
import numpy as np
import pandas as pd 

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Set up database engine for flask app
#Use create_engine() to access and query SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create a variable for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link from Python to our database
session = Session(engine)

#Set up Flask
app = Flask(__name__)

#Define the welcome route
@app.route("/")

#Add the routes we will need in the return statement
#/api/1v.0/ followed by the route name is a convention that signifies this is version 1 of our app
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#Create a new route for precipitation
@app.route("/api/v1.0/precipitation")

#Create the precip function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #write a query to get the date and precip for previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Create the stations route
@app.route("/api/v1.0/stations")



@app.route("/api/v1.0/stations")

def stations():
	results = session.query(Station.station).all()
	# Unravel results into one-dimensional array with:
		# `function np.ravel()`, `parameter = results`
	# Convert results array into a list with `list()`
	stations = list(np.ravel(results))
	return jsonify(stations=stations) 

# NOTE: `stations=stations` formats the list into JSON
# NOTE: Flask documentation: https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify



@app.route("/api/v1.0/tobs")

def temp_monthly():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	results = session.query(Measurement.tobs).\
		filter(Measurement.station == 'USC00519281').\
		filter(Measurement.date >= prev_year).all()
	temps = list(np.ravel(results))
	return jsonify(temps=temps)


# Provide both start and end date routes:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Add parameters to `stats()`: `start` and `end` parameters
def stats(start=None, end=None):
	# Query: min, avg, max temps; create list called `sel`
	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

	# Add `if-not` statement to determine start/end date
	if not end:
		results = session.query(*sel).\
			filter(Measurement.date >= start).\
			filter(Measurement.date <= end).all()
		temps = list(np.ravel(results))
	return jsonify(temps=temps)

		# NOTE: (*sel) - asterik indicates multiple results from query: minimum, average, and maximum temperatures

	# Query: Calc statistics data
	results = session.query(*sel).\
		filter(Measurement.date >= start).\
		filter(Measurement.date <= end).all()
	temps = list(np.ravel(results))
	return jsonify(temps=temps)

	# NOTE: /api/v1.0/temp/start/end route -> [null,null,null]
	# NOTE: Add following to path to address in browser:
		# /api/v1.0/temp/2017-06-01/2017-06-30
		# result: ["temps":[71.0,77.21989528795811,83.0]]
