import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setting up database


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



# Flask Setup

app = Flask(__name__)


#################################################
# Flask Routes
#################################################



@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Returns total numbers of precipation from previous years by station.<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"Returns station location and id.<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Returns temperature observed in stations from previous years<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"Returns the MIN, AVG, and MAX temperatures for dates greater than and equal to the start date.<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Returns the MIN, AVG, and MAX temperatures for dates between the start and end date.<br/>"
    )
####################################################
#/api/v1.0/precipitation
#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
####################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for last year"""
# Create our session (link) from Python to the DB
    session = Session(engine)


# Query for the dates and precipitation observations from the last year.
    Max_date = session.query(func.max(Measurement.date)).first()
    
    # Get the first element of the tuple
    max_date = max_date[0]
    
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(365)
    one_year_ago

    results = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date > '2016-08-23').all()
                                                                    
    # Convert list of tuples into normal list
    precipitation_dict = dict(results)

    return jsonify(precipitation_dict)


#/api/v1.0/stations
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Query stations
    results_stations =  session.query(Measurement.station).group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results_stations))

    return jsonify(stations_list)


#/api/v1.0/tobs

#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(365)
    one_year_ago

    query_date_temp = session.query(Measurement.tobs,Measurement.date).\
                        order_by(Measurement.date).\
                        filter(Measurement.date>=one_year_ago).all()
    
    query_temp_df = pd.DataFrame(query_date_temp,columns=['temp observed','date'])
    query_temp_df.set_index('date',inplace=True)

    return jsonify(query_temp_df.to_dict())



if __name__ == "__main__":
    app.run(debug=True)