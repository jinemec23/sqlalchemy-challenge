from os import name
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import date, timedelta

from flask import Flask, jsonify

from flask import Flask

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def index():
    "List all routes that are available"
    return (
        f"Available Routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;</br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;</br>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    session.close()

    precipitation = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date']= date
        prcp_dict['prcp']= prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    station_results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    session.close()

    stations = []

    for station in station_results:
        station_dict = {}
        station_dict['Station']= station
        stations.append(station_dict)


    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = (dt.datetime.strptime(recent_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_date).\
            order_by(Measurement.date).all()
    
    session.close()
  

    date_tobs = []

    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        date_tobs.append(tobs_dict)



    return jsonify(date_tobs)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)

    start_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            group_by(Measurement.date).all()
    
    session.close()


    tobs_start = []

    for min,max,avg in start_query:
        start_dict = {}
        start_dict["date"] = date
        start_dict["TMIN"] = min
        start_dict["TMAX"] = max
        start_dict["TAVG"] = avg
        tobs_start.append(start_dict)
    

    return jsonify()

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    session = Session(engine)

    start_end_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).\
            group_by(Measurement.date).all()
    session.close()

    tobs_start_end = []

    for min,max,avg in start_end_query:
        start_end_dict = {}
        start_end_dict["date"] = date
        start_end_dict["TMIN"] = min
        start_end_dict["TMAX"] = max
        start_end_dict["TAVG"] = avg
        tobs_start_end.append(start_end_dict)


    return jsonify()

if __name__ == "__main__":
    app.run(debug=True)

