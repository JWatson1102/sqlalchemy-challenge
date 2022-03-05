from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy import desc
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
#####################################################################
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
year_ago

# Perform a query to retrieve the data and precipitation scores
begin_date = dt.datetime(2016, 8, 23)

last_12_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > begin_date).all()

precip_dates = []
prcps = []
for row in last_12_months:
    precip_dates.append(row[0])
    prcps.append(row[1])

#####################################################################
active_stations = []
station_counts = []
station_count_list = []

for row in session.execute('SELECT station, COUNT(station) AS count FROM measurement GROUP BY station ORDER BY count DESC'):
    active_stations.append(row[0])
    station_counts.append(row[1])
    station_count_list.append(row)

most_active_station = active_stations[0]
#####################################################################
stations = []
for station in session.query(Station.station):
    stations.append(station)
stations
#####################################################################
yearly_temp = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > begin_date, Measurement.station == most_active_station)

temp_dates = []
temps = []
for row in yearly_temp:
    temp_dates.append(row[0])
    temps.append(row[2])
#####################################################################
precip_dict = {precip_dates[i]: prcps[i] for i in range(0, len(precip_dates))}
temp_dict = {temp_dates[i]: temps[i] for i in range(0, len(temp_dates))}
#####################################################################
@app.route("/")
def home():
    return (
        f"These are the available routes:<br/> "
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precitipation():
    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def station_api():
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(temp_dict)

@app.route('/api/v1.0/<start>')
def begin_search(start):
    return(
        session.query(Measurement.date,func.min(Measurement.tobs),\
            func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter_by(Measurement.date >= start)
        )

@app.route('/api/v1.0/<start><end>')
def begin_end_search(start,end):
    return(
        session.query(Measurement.date,func.min(Measurement.tobs),\
            func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter_by(Measurement.date >= start and Measurement.date <=end)
    )
    

if __name__ == "__main__":
    app.run(debug=True)
