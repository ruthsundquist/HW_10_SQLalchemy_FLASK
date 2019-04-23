# 1. import Flask
import numpy as np
import pandas as pd
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


start_date = '2012-02-28'
end = '2012-03-11'


def start(data):
    data_dict = {"TMIN":data[0][0],
                 "TMAX":data[0][1],
                 "TAVG":data[0][2]}
    return(jsonify(data_dict))


# 2. Create an app

app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/stations<br/>"
        f"/api/precipitation<br/>"
        f"/api/temperature<br/>"
        f"/api/start<br/>"
        f"api/<start>/<end>"

    )
@app.route("/api/precipitation")
def precipitation():
    raintotal=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2011-02-28").\
    filter(Measurement.date <=  "2012-03-11")
    raintotal_dict ={}
    for date in list(raintotal): #for each date
        raintotal_dict[date[0]] = date[1]  #assign the date as key
        
    return jsonify(raintotal_dict)
   
@app.route("/api/stations")
def stations():
    stations=session.query(Station.station)
    
    
        
    return jsonify(list(stations))

@app.route("/api/temperature")
def temperature():
    temperature = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2011-02-28").\
    filter(Measurement.date <=  "2012-03-11")
    return jsonify(list(temperature))
  



@app.route("/api/2012-02-28")
def start_full():
    data = session.query(func.min(Measurement.tobs),
                         func.max(Measurement.tobs),
                         func.avg(Measurement.tobs)).\
                         filter(Measurement.date >= "2012-02-28")
    return(start(data))

@app.route("/api/2012-02-28_2012-03-11")
def start_ranged(start_date,end):
    data = session.query(func.min(Measurement.tobs),
                         func.max(Measurement.tobs),
                         func.avg(Measurement.tobs)).\
                         filter(Measurement.date >= "2012-02-28").\
                         filter(Measurement.date <= "2012-03-11")
    return(start(data))
    
    
#def home():


if __name__ == "__main__":
    app.run(debug=True,threaded=False)