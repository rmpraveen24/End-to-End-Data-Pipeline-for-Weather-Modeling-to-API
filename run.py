import sqlite3
from app import app, db
from models import Weather, WeatherStats
from datetime import datetime


def seed_data():
    # Connecting to the database and fetching the Weather Data and Weather Stats data

    conn = sqlite3.connect('CortevaDB.db')  # Connect to your SQLite database file
    conn.row_factory = sqlite3.Row
    print("==================Connected to the DB successfully==================")

    # Query data from 'Weather_Data' and 'Weather_Stats' tables in SQLite3
    weather_query = conn.execute('SELECT * FROM Weather_Data').fetchall()
    stats_query = conn.execute('SELECT * FROM Weather_stats').fetchall()
    print("==================Records fetched from the DB successfully==================")

    conn.close()  # Close the connection after fetching data

    # Process and add weather data to SQLAlchemy session
    sample_weather = []  #Storing the Weather data in the empty list
    for row in weather_query:
        sample_weather.append(
            Weather(
                STATION_ID=row['STATION_ID'],
                DATE=datetime.strptime(row['DATE'], '%Y-%m-%d').date(),
                YEAR=row['YEAR'],
                MONTH=row['MONTH'],
                DAY=row['DAY'],
                MAX_TEMP=round(row['MAX_TEMP'], 2),
                MIN_TEMP=round(row['MIN_TEMP'],2),
                PRECIPITATION=row['PRECIPITATION']
            )
        )

    # Process and add weather stats data to SQLAlchemy session
    sample_stats = []  #Storing the Weather Stats data in the empty list
    for row in stats_query:
        sample_stats.append(
            WeatherStats(
                STATION_ID=row['STATION_ID'],
                YEAR=datetime.strptime(row['YEAR'],'%Y-%m-%d').year,
                AVG_MAX_TEMP=round(row['AVG_MAX_TEMP'],2),
                AVG_MIN_TEMP=round(row['AVG_MIN_TEMP'],2),
                TOTAL_PRECIPITATION=row['TOTAL_PRECIPITATION']
            )
        )


    db.session.bulk_save_objects(sample_weather)
    db.session.bulk_save_objects(sample_stats)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
