# Import dependencies.
import datetime as dt
import numpy as np
import pandas as pd

# Add SQLAlchemy dependencies, allow us to use SQLite
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Add dependencies for Flask
from flask import Flask, jsonify

# Setup database engine to access SQLite database.
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

# Define our Flask app. This will create a Flask application called "app."
app = Flask(__name__)



# Define the welcome route.
@app.route("/")

# Add the routing information for each of the other routes
# Add the precipitation, stations, tobs, and temp routes that we'll need for this module
def welcome():
    return('''
    
    Welcome to the Climate Analysis API!
    Available Routes:
    
    /api/v1.0/precipitation
    
    /api/v1.0/stations
    
    /api/v1.0/tobs
    
    /api/v1.0/temp/start/end
    
    ''')
    
# The next route we'll build is for the precipitation analysis with the precipitation() function.
# Add a query to get the date and precipitation for the previous year.
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

    return

# Create the stations route.
# Create a query that will allow us to get all of the stations in our database.
# Convert our unraveled results into a list. To convert the results to a list, we will need to use the list function.
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create the monthly temperature function
# Calculate the date one year ago from the last date in the database
# Query the primary station for all the temperature observations from the previous year
# Unravel the results into a one-dimensional array and convert that array into a list. 
# Then jsonify the list.
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create a route for summary statistics report. 
# This route is different from the previous ones in that we will have to provide both a starting and ending date.
# Create a function called stats() to put our code in.
# Add parameters to our stats()function: a start parameter and an end parameter. For now, set them both to None.
# Create a query to select the minimum, average, and maximum temperatures from our SQLite database. Create a list called sel
# Determine the starting and ending date, add an if-not statement to our code. We'll need to query our database using the list 
# Unravel the results into a one-dimensional array and convert them to a list. 
# jsonify our results and return them.

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
