

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement=Base.classes.measurement

station=Base.classes.station


session = Session(engine)


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# Home page.


#List all routes that are available.

@app.route("/")
def welcome():
    return (
        f"Welcome to Home Page!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"<br/>"
        f"List of the rainfall from previous years"
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation"
        f"<br/>"
        f"<br/>"
        f"List of Stations"
         f"<br/>"
         f"<br/>"
        f"/api/v1.0/stations"
         f"<br/>"
         f"<br/>"
        f"The dates and temperature observations of the most active station for the last year of data" 
        f"<br/>"
         f"<br/>"
        f"/api/v1.0/tobs"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
   
    

    date=dt.date(2017,8,23)

    one_year_date=date-dt.timedelta(days=365)
   
    date_prcp=session.query(measurement.date,measurement.prcp).filter(measurement.date>one_year_date).order_by(measurement.date).all()
    

    precipitation_total= []
    for x in date_prcp:
    
        rain = {}
        rain["date"] = x[0]
        rain["prcp"] = x[1]
        precipitation_total.append(rain)

    return jsonify(precipitation_total)


@app.route("/api/v1.0/stations")
def stations():


    locations=session.query(station.station)


    df_locations=pd.DataFrame(locations)


   

    session.close()

    
    all_locations= list(np.ravel(df_locations))

    return jsonify(all_locations)

@app.route("/api/v1.0/tobs")
def temperature ():
    date=dt.date(2017,8,23)

    one_year_date=date-dt.timedelta(days=365)

    count_=func.count(measurement.station)
    active_stations=session.query(measurement.station,count_).group_by(measurement.station).order_by(count_.desc()).all()
    


    most_active=active_stations[0][0]

    last_twelve_most_active=session.query(measurement.date,measurement.tobs).filter(measurement.station==most_active,measurement.date>one_year_date).all()

    last_twelve_most_active=pd.DataFrame(last_twelve_most_active)


    


    session.close()

    
    temperatures= list(np.ravel(last_twelve_most_active))

    return jsonify(temperatures)



@app.route("/api/v1.0/<start>")
def start_only(start):


    start_date=dt.datetime.strptime(start,'%Y-%m-%d')

    one_year=dt.timedelta(days=365)

    start_d=start_date-one_year

    end_date=dt.date(2017,8,23)





    all_datas=session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date>=start_d).filter(measurement.date<=end_date).all()
   


    
    all_datas_list= list(np.ravel(all_datas))
    return jsonify(all_datas_list)



@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start,end):

    start_date=dt.datetime.strptime(start,'%Y-%m-%d')

    end_date=dt.datetime.strptime(end,'%Y-%m-%d')

    one_year=dt.timedelta(days=365)

    start_d=start_date-one_year
    
    end_d=end_date-one_year

    all_minmaxavg=session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date>=start_d).filter(measurement.date<=end_d).all()

    all_minmaxavg_list= list(np.ravel(all_minmaxavg))
    return jsonify(all_minmaxavg_list)

if __name__ == "__main__":
    app.run(debug=True)