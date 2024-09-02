# Import the dependencies.

import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine(r"sqlite:///C:/Projects/sqlalchemy_challenge/SurfsUp/resources/hawaii.sqlite")

# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Helper Function to Calculate Dates
#################################################


def calculate_dates():
    # Query for the most recent date
    max_date_str = session.query(func.max(Measurement.date)).scalar()
    
    # Convert to date time
    max_date = dt.datetime.strptime(max_date_str, "%Y-%m-%d")

    # Calculate the date one year earlier
    min_date = max_date - dt.timedelta(days=365)

    return max_date, min_date


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/2010-12-11'>/api/v1.0/2010-12-11</a><br/>"
        f"<a href='/api/v1.0/2012-10-15/2012-12-15'>/api/v1.0/2012-10-15 through 2012-12-15/a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query your data for the last 12 months of precipitation data
    max_date, min_date = calculate_dates()   
    
    # Query for the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= min_date).all()

    # Convert the query results to a dictionary
    precip_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Query for station information
    stations_data = session.query(Station.station).all()

    # Convert the query results to a list
    stations_list = list(np.ravel(stations_data))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the dates for the last year of data
    max_date, min_date = calculate_dates()

    # Query the temperature observations of the most active station for the last year
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= min_date).all()

    # Convert the query results to a list
    tobs_list = list(np.ravel(tobs_data))

    return jsonify(tobs_list)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):

    # Convert start and end to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    try:
        # If no end date provided, assume end date as the most recent date in the dataset
        if not end:
            end_date = session.query(func.max(Measurement.date)).scalar()
        else:
            end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        
        # Query to get TMIN, TAVG, TMAX for the date range
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        results = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
        # Close the session
        session.close()
        
        # Create a dictionary for the results
        temps = {
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }
        
        return jsonify(temps)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
