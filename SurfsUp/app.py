# Import the dependencies.

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

from flask import Flast, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///resources?hawaii.sqlite")

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
# Flask Routes
#################################################

def calculate_dates():
    Parameters:
    None

    Returns:
    max_date(datetime): Most recent date
    min_date(datetime): Date one year earlier

session = Session(engine)

# Query for measurement dates
date_finder = session.query(Measurement.date)
date_finder_max = max(date_finder)

# convert to date time
max_date = dt.datetime.strptime(date_finder_max[0], "&Y-%m-%d" )

# Calculate the date one year from last
min_date = max_date - dt.timeIta(days=366)

#Close session
session.close()

return max_date, min_date

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query your data for the last 12 months of precipitation data
    # Example:
    # results = session.query(Measurement.date, Measurement.prcp).filter(...).all()
    
    # Convert the query results to a dictionary
    precip_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query your data for station information
    # Example:
    # results = session.query(Station.station).all()
    
    stations_list = list(np.ravel(stations_data))
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query your data for temperature observations of the most active station
    # Example:
    # results = session.query(Measurement.date, Measurement.tobs).filter(...).all()
    
    tobs_list = list(np.ravel(tobs_data))
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    # If only start date is provided
    if end:
        results = start_end_data.query.filter(...).all()  # Include logic for both start and end
    else:
        results = start_end_data.query.filter(...).all()  # Include logic for start only
    
    temps = {
        "TMIN": min([r[0] for r in results]),
        "TAVG": np.mean([r[1] for r in results]),
        "TMAX": max([r[2] for r in results]),
    }
    
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)




