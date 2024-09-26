import sqlite3
from datetime import datetime, date
import pandas as pd
import logging


def Read_weather_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('CortevaDB.db')

        # Read the data from the 'weather_data' table into a DataFrame
        query = "SELECT STATION_ID, DATE, MAX_TEMP, MIN_TEMP, PRECIPITATION FROM Weather_data"
        df = pd.read_sql_query(query, conn)

        # Convert 'DATE' column to datetime format for easier manipulation
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')

        print(df.head(5))

        # Close the connection
        conn.close()
        return df

    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)

def data_analysis(df):
    try:
        # Removing rows where temperature and precipitation data is missing (-9999)
        df = df[(df['MAX_TEMP'] != -9999) & (df['MIN_TEMP'] != -9999) & (df['PRECIPITATION'] != -9999)]

        # Adding a 'YEAR' column to group data by year
        df['YEAR'] = df['DATE'].dt.year

        # Convert temperature from tenths of degrees Celsius to degrees Celsius
        df['MAX_TEMP'] = df['MAX_TEMP'] / 10.0
        df['MIN_TEMP'] = df['MIN_TEMP'] / 10.0
        print(df['PRECIPITATION'][0])
        # Convert precipitation from tenths of millimeters to centimeters
        df['TOTAL_PRECIPITATION'] = df['PRECIPITATION'] / 100.0

        #print(df['TOTAL_PRECIPITATION'][0])

        # Group by 'STATION_ID' and 'YEAR' and calculate the required statistics
        grouped = df.groupby(['STATION_ID', 'YEAR']).agg(
            avg_max_temp=('MAX_TEMP', 'mean'),
            avg_min_temp=('MIN_TEMP', 'mean'),
            total_precipitation=('TOTAL_PRECIPITATION', 'sum')
        ).reset_index()

        #print(grouped)
        return grouped



    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)


def weather_stats(computation):
    try:

        # Connect to the SQLite database
        conn = sqlite3.connect('Cortevadb.db')

        # Creating a cursor object to interact with the database
        cursor = conn.cursor()

        # Create the 'weather_stats' table if it doesn't exist
        cursor.execute('''
        CREATE TABLE  Weather_Stats (
            STATION_ID TEXT NOT NULL,
            YEAR INTEGER NOT NULL,
            AVG_MAX_TEMP REAL,
            AVG_MIN_TEMP REAL,
            TOTAL_PRECIPITATION REAL  
        );
        ''')
#PRIMARY KEY (STATION_ID, YEAR)

        # Insert the grouped data into the 'weather_stats' table
        computation.to_sql('Weather_Stats', conn, if_exists='append', index=False)

        # Commit and close the connection
        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)




def main():
    try:
        global conn
        #================= START LOG FILE=======================================
        logging.basicConfig(filename='LOG_Data_analysis.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

        # Log the start time
        start_time = datetime.now()
        logging.info(f"Data ingestion started at {start_time}")

        #====================DATA ANALYSIS==========================
        df=Read_weather_data()

        computation=data_analysis(df)

        weather_stats(computation)


        end_time = datetime.now()
        logging.info(f"Data ingestion completed at {end_time}")

        #=================END LOG FILE=======================================


    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)
    '''finally:
        if conn:
            conn.close()'''

if __name__=='__main__':
    main()