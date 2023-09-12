import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Flask Setup
app = Flask(__name__)
# Flask Routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )
##================================================
##FROM THIS POINT FORWARD THE CODE IS NOT CORRECT - IT WILL BE SUBMITTED AGAIN

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    One_Year_Earlier = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data_precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= One_Year_Earlier).all()
    session.close()
    one_year_weather = []
    for date, prcp in data_precip_scores:
        date_rain = {}
        date_rain["date"] = date
        date_rain["prcp"] = prcp
        one_year_weather.append(date_rain)
    return jsonify(one_year_weather)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_names = session.query(Station.name, Station.id, Station.elevation, Station.longitude, Station.latitude, Station.station).all()
    session.close()
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    waihee_city = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23') \
    .filter(Measurement.date <= '2017-08-23').all()
    session.close()
    return jsonify(waihee_city)



#one_year_weather = [{"date": date, "prcp": prcp} for date, prcp in data_precip_scores]



if __name__ == '__main__':
    app.run(debug=True)















