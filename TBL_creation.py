import sqlite3

'''Making connection to the database  and the data base was created using CMD'''

conn = sqlite3.connect('Cortevadb.db')

# Creating a cursor object to interact with the database
cursor = conn.cursor()

# Creating the weather_data table with specified fields as below
cursor.execute('''
    CREATE TABLE Weather_Data (
    RECORD_ID TEXT PRIMARY KEY ,
    STATION_ID TEXT NOT NULL,
    DATE INTEGER NOT NULL,
    YEAR INTEGER NOT NULL,
    MONTH INTEGER NOT NULL,
    DAY INTEGER NOT NULL,
    MAX_TEMP REAL,
    MIN_TEMP REAL,
    PRECIPITATION REAL
);
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Table 'Weather_data' created successfully!")