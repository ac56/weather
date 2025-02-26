from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "data", "weather.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/locations")
def list_locations():
    conn = get_db_connection()
    locations = conn.execute("SELECT DISTINCT location FROM weather_data").fetchall()
    conn.close()
    return jsonify([dict(row) for row in locations])

@app.route("/daily_forecasts")
def list_daily_forecasts():
    conn = get_db_connection()
    daily_forecasts = {}
    forecasts = conn.execute("SELECT * FROM weather_data ORDER BY date_time").fetchall()
    for row in forecasts:
        location = row['location']
        date = datetime.strptime(row['date_time'], '%Y-%m-%d %H:%M:%S').date()
        date_str = date.strftime('%Y-%m-%d')
        if location not in daily_forecasts:
            daily_forecasts[location] = {}
        if date_str not in daily_forecasts[location]:
            daily_forecasts[location][date_str] = {
                'temperature': {'min': float('inf'), 'max': float('-inf')},
                'precipitation': {'min': float('inf'), 'max': float('-inf')},
                'wind_speed': {'min': float('inf'), 'max': float('-inf')}
            }

        daily_forecasts[location][date_str]['temperature']['min'] = min(daily_forecasts[location][date_str]['temperature']['min'], row['temperature'])
        daily_forecasts[location][date_str]['temperature']['max'] = max(daily_forecasts[location][date_str]['temperature']['max'], row['temperature'])
        daily_forecasts[location][date_str]['precipitation']['min'] = min(daily_forecasts[location][date_str]['precipitation']['min'], row['precipitation'])
        daily_forecasts[location][date_str]['precipitation']['max'] = max(daily_forecasts[location][date_str]['precipitation']['max'], row['precipitation'])
        daily_forecasts[location][date_str]['wind_speed']['min'] = min(daily_forecasts[location][date_str]['wind_speed']['min'], row['wind_speed'])
        daily_forecasts[location][date_str]['wind_speed']['max'] = max(daily_forecasts[location][date_str]['wind_speed']['max'], row['wind_speed'])

    conn.close()
    return jsonify(daily_forecasts)

@app.route("/avg_temp")
def avg_temp():
    conn = get_db_connection()
    last_3_avg_temps = {}
    forecasts = conn.execute("SELECT * FROM weather_data ORDER BY date_time").fetchall()
    for row in forecasts:
        location = row['location']
        date = datetime.strptime(row['date_time'], '%Y-%m-%d %H:%M:%S').date()
        date_str = date.strftime('%Y-%m-%d')
        if location not in last_3_avg_temps:
            last_3_avg_temps[location] = {}
        if date_str not in last_3_avg_temps[location]:
            last_3_avg_temps[location][date_str] = []
        last_3_avg_temps[location][date_str].append(row['temperature'])

    for location in last_3_avg_temps:
        for date in last_3_avg_temps[location]:
            if len(last_3_avg_temps[location][date]) >= 3:
                last_3_avg_temps[location][date] = sum(last_3_avg_temps[location][date][-3:]) / 3
            else:
                last_3_avg_temps[location][date] = None

    conn.close()
    return jsonify(last_3_avg_temps)

@app.route("/top_locations")
def top_locations():
    metric = request.args.get("metric")
    n = request.args.get("n", default=3, type=int)

    if metric not in ["temperature", "precipitation", "wind_speed"]:
        return jsonify({"error": "Invalid metric"}), 400

    if n not in [1,2,3]:
        return jsonify({"error": "n must be 1,2, or 3"}), 400

    conn = get_db_connection()
    top_locations_data = conn.execute(f"""
        SELECT location, AVG({metric}) AS avg_metric
        FROM weather_data
        GROUP BY location
        ORDER BY avg_metric DESC
        LIMIT ?
    """, (n,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in top_locations_data])

if __name__ == "__main__":
    app.run(debug=True)