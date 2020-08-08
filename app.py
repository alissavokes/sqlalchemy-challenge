import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta as rd

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask setup
app = Flask(__name__)

#flask routes
@app.route("/")
def welcome():
    return(f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/08232016<br/>"
            f"/api/v1.0/08232016/12312016<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session
    session = Session(engine)

    #gather relevant info for query
    #view latest date in table
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.date(2017,8,23)
    year_before_last_date = dt.date(2017, 8, 23) - rd(months=+12)
    #perform query
    precip_prior_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before_last_date, 
                                                                                    Measurement.date <= last_date).all()
    #close session
    session.close()

    precip_data = []
    for date, precip in precip_prior_year:
        precip_dict = {}
        precip_dict[date] = precip #make date key and precipitation info value
        precip_data.append(precip_dict)

    #return json representation
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    #create session
    session = Session(engine)
   
    #perform query
    list_stations = session.query(Station.station, Station.name).all()

    #close session
    session.close()

    station_info = []
    for station, name in list_stations:
        station_dict = {}
        station_dict[station] = name #make station key and name value
        station_info.append(station_dict)

    #return json representation
    return jsonify(station_info)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)
    
    #gather relevant info for query
    #from hw pt 1: Which station has the highest number of observations? USC00519281
    #view latest date in table
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.date(2017,8,23)
    year_before_last_date = dt.date(2017, 8, 23) - rd(months=+12)

    #perform query
    station_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281", 
                                                            Measurement.date >= year_before_last_date, 
                                                            Measurement.date <= last_date).all()

    #close session
    session.close()

    tobs_data = []
    for date, tobs in station_tobs:
        tobs_dict = {}
        tobs_dict[date] = tobs #make date key and precipitation info value
        tobs_data.append(tobs_dict)

    #return json representation
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    start = dt.datetime.strptime(start, "%m%d%Y")
    #create session
    session = Session(engine)
   
    #perform query
    sel = [func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]

    measurement_data = session.query(*sel).filter(Measurement.date >= start).all()

    #close session
    session.close()

    tobs_info = []
    for minimum, average, maximum in measurement_data:
        tobs_dict = {}
        tobs_dict["min temp"] = minimum
        tobs_dict["avg temp"] = average
        tobs_dict["max temp"] = maximum
        tobs_info.append(tobs_dict)

    #return json representation
    return jsonify(tobs_info)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    #create session
    session = Session(engine)
   
    #perform query
    sel = [func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)]

    measurement_data = session.query(*sel).filter(Measurement.date >= start, Measurement.date <= end).all()

    #close session
    session.close()

    tobs_info = []
    for minimum, average, maximum in measurement_data:
        tobs_dict = {}
        tobs_dict["min temp"] = minimum
        tobs_dict["avg temp"] = average
        tobs_dict["max temp"] = maximum
        tobs_info.append(tobs_dict)

    #return json representation
    return jsonify(tobs_info)


if __name__ == '__main__':
    app.run(debug=True)
