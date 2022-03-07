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
session.close()


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
session.close()

most_active_station = active_stations[0]
#####################################################################
stations = []
for station in session.query(Station.station):
    stations.append(station)
stations
session.close()
#####################################################################
yearly_temp = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > begin_date, Measurement.station == most_active_station)
session.close()
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
        f"These are the available routes:<br> "
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
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

@app.route('/api/v1.0/<search_start>')
def begin_search(search_start):
    print(f"I'm running the search_start: {search_start}")
    #search_start = dt.datetime.strptime(search_start, "%Y-%m-%d")
    temps = []
    for day in temp_dict:    
        #print((day))
        if day >= search_start:
            temps.append(temp_dict[day])

    return (f"Mean Temperature: {sum(temps)/len(temps)} <br>Min Temp: {min(temps)} <br>Max Temp: {max(temps)}")

@app.route('/api/v1.0/<search_start>/<search_end>')
def begin_end_search(search_start, search_end):
    print(f"I'm running the search_start: {search_start}")
    #search_start = dt.datetime.strptime(search_start, "%Y-%m-%d")
    temps = []
    for day in temp_dict:    
        #print((day))
        if day >= search_start and day <= search_end:
            temps.append(temp_dict[day])
    return (f"Mean Temperature: {sum(temps)/len(temps)} <br>Min Temp: {min(temps)} <br>Max Temp: {max(temps)}")
    


    

if __name__ == "__main__":
    app.run(debug=True)
