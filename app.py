# Import the dependencies.
from flask import Flask, jsonify

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import datetime

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text
from collections import defaultdict 


#################################################
# Database Setup
#################################################

#C:\Users\schre\OneDrive\Documents\GitHub\sqlalchemy-challenge\Resources\hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///C:/Users/schre/OneDrive/Documents/GitHub/sqlalchemy-challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station


# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather stations and precipitation API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )



#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precip():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    q=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()


    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    date_info_df=pd.DataFrame(q)
    date_info_df


    # Sort the dataframe by date
    date_sorted=date_info_df.sort_values("date")
    date_sorted
    #print(date_sorted.index)

    #date_index=date_sorted.reset_index(drop=True)
    
    newdf=pd.DataFrame(date_sorted.groupby('date').sum())
    #print(newdf)

    date_dict=newdf.to_dict()

    #print(date_dict)

#
    return(jsonify(date_dict['prcp']))

@app.route("/api/v1.0/stations")
def stations():
    #q2=session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    q2=session.query(Station.station).all()
    #print(q2)
    q2=pd.DataFrame(q2).to_dict()
    return(q2)


#Returns jsonified data for the most active station (USC00519281) (3 points)
#Only returns the jsonified data for the last year of data (3 points)
@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    q3=session.query(Measurement.station, Measurement.prcp, Measurement.tobs).filter(Measurement.date >= query_date).\
    filter(Measurement.station == 'USC00519281').all()
    q3=pd.DataFrame(q3).to_dict()
    return(jsonify(q3))

#Dynamic Routes
@app.route("/api/v1.0/<start>")
def dyn1(start):
    q4=session.query(Measurement.tobs).filter(Measurement.date >= start).all()
    print(q4)

    test=[]
    for item in q4:
        a1=str(item).replace(",", "")
        a2= a1.replace('(', '').replace(')', '')
        test.append(float(a2))

    #TMIN, TAVG, and TMAX
    TMIN=min(test)
    TMAX=max(test)
    TAVG=np.mean(test)
    
    return(jsonify([TMIN, TAVG, TMAX]))


@app.route("/api/v1.0/<start>/<end>")
def dyn2(start,end):
    q5=session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    print(q5)

    test=[]
    for item in q5:
        a1=str(item).replace(",", "")
        a2= a1.replace('(', '').replace(')', '')
        test.append(float(a2))

    #TMIN, TAVG, and TMAX
    TMIN=min(test)
    TMAX=max(test)
    TAVG=np.mean(test)
    
    return(jsonify([TMIN, TAVG, TMAX]))


if __name__ == "__main__":
    app.run(debug=True)