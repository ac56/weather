from datetime import datetime, timedelta
import sqlite3
# import json
import os
import csv
import requests



BASE_URL = "https://api.meteomatics.com/"
USERNAME = "margera_constantinou_alexandros"  # Replace with your username
PASSWORD = "4xmVW2Otf1"  # Replace with your password

LOCATIONS = {
    "Nicosia": {"lat": 35.18, "lon": 33.38},
    "Athens": {"lat": 37.98, "lon": 23.73},
    "Rome": {"lat": 41.90, "lon": 12.49},
}
DAYS = 7
METRICS = ["t_2m:C", "precip_1h:mm", "wind_speed_10m:ms"]

def get_weather_data(lat, lon, start_date, end_date, metrics):
    """Retrieves weather data for a given latitude, longitude, and date range."""
    base_url = "https://api.meteomatics.com/"
    metrics_str = ",".join(metrics)
    location_str = f"{lat},{lon}"
    time_range = f"{start_date.strftime('%Y-%m-%dT00:00:00Z')}--{end_date.strftime('%Y-%m-%dT23:00:00Z')}:PT1H"
    url = f"{base_url}{time_range}/{metrics_str}/{location_str}/json"

    try:
        response = requests.get(url, auth=(USERNAME, PASSWORD), timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and data['data']:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting weather data: {e}")
        return None
    
def export_to_csv(db_path, csv_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([description[0] for description in cursor.description])  # Write header
            writer.writerows(rows)

        conn.close()
        print(f"Data exported to {csv_path}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def fetch_and_store_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "data", "weather.db")
    csv_path = os.path.join(script_dir, "..", "data", "weather.csv")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            location TEXT,
            date_time TEXT,
            temperature REAL,
            precipitation REAL,
            wind_speed REAL,
            PRIMARY KEY (location, date_time)
        )
    """)

    for location_name, coordinates in LOCATIONS.items():
        lat = coordinates["lat"]
        lon = coordinates["lon"]
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=(DAYS-1))
        weather_data = get_weather_data(lat, lon, start_date, end_date, METRICS)
        if weather_data and weather_data['data']:
            combined_data = {}
            for param in weather_data['data']:
                parameter_name = param['parameter']
                for coord in param['coordinates']:
                    lat = coord['lat']
                    lon = coord['lon']
                    for date_entry in coord['dates']:
                        date_time = date_entry['date']
                        value = date_entry['value']
                        key = (lat, lon, date_time)
                        if key not in combined_data:
                            combined_data[key] = {'lat': lat, 'lon': lon, 'date_time': date_time}
                        combined_data[key][parameter_name] = value

            combined_data_list = list(combined_data.values())

            for item in combined_data_list:
                try:
                    date_time = datetime.strptime(item['date_time'], '%Y-%m-%dT%H:%M:%SZ')
                    cursor.execute("""
                        INSERT OR REPLACE INTO weather_data (location, date_time, temperature, precipitation, wind_speed)
                        VALUES (?, ?, ?, ?, ?)
                    """, (location_name, date_time.strftime('%Y-%m-%d %H:%M:%S'),
                          item.get('t_2m:C'), item.get('precip_1h:mm'), item.get('wind_speed_10m:ms')))
                except (ValueError, KeyError) as e:
                    print(f"Error inserting data for {location_name}, {item.get('date_time')}: {e}")

    
    conn.commit()
    conn.close()
    export_to_csv(db_path, csv_path, "weather_data")

fetch_and_store_data()