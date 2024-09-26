import traceback
import sqlite3
from datetime import datetime, date
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import logging


#==============================================================================
'''All the below hard coding can be stored in JSON file : URL, Credentials etc'''


# GitHub repository details
owner = "corteva"
repo = "code-challenge-template"
branch = "main"
directory = "wx_data"


# Add your GitHub username and personal access token here
username = "rmpraveen24"
token = "24Eight@95"

# GitHub API URL to get the contents of the directory
api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{directory}?ref={branch}"

#=========================================================================================

def data_process(api_url,username,token):
    try:

        # Fetch the list of files in the directory with authentication
        response = requests.get(api_url, auth=HTTPBasicAuth(username, token))

        if response.status_code == 200:
            try:
                # Parse the JSON response
                files = response.json()

                n=0
                data = []
                # List the file names
                print("Files in the GitHub directory:")
                for file in files:

                    data_path="https://raw.githubusercontent.com/corteva/code-challenge-template/main/wx_data"+"/"+file['name']
                    #print(type(file['name']))

                    filename=file['name']
                    if filename.endswith('.txt'):

                        station_id= filename.replace(".txt", "")
                        #print(station_id)

                        #print(data_path)

                        Text_response = requests.get(data_path)
                        if Text_response.status_code ==200:
                            file_content = Text_response.text
                            lines=file_content.splitlines()
                            a=0

                            for line in lines:
                                weat_data= line.split()

                                weat_data.insert(0,station_id)
                                rec_id = station_id + "-" + weat_data[1]
                                weat_data.insert(0, rec_id)
                                #print(type(weat_data[2]))

                                year = str(weat_data[2])[:4]
                                month = str(weat_data[2])[4:6]
                                day = str(weat_data[2])[6:]

                                dt_time=[year ,month, day]
                                weat_data[3:3]=dt_time

                                data.append(weat_data)
                                a+=1
                                '''if a==3:
                                    break'''
                            print(f"The data has been processed for :{n}....{station_id}")
                            logging.info(f"The data has been processed for :{n}....{station_id}")
                            n += 1

                        '''if n==1:
                            break'''

                df = pd.DataFrame(data, columns=['RECORD_ID','STATION_ID', 'DATE', 'YEAR','MONTH','DAY','MAX_TEMP', 'MIN_TEMP', 'PRECIPITATION']) #,'DATE_PROCESSED'

                #print(type(df['DATE']))

                df['DATE'] = df['DATE'].astype('int64')

                print(df)

                print("Total number of values in the DataFrame:", df.shape[0])
                logging.info(f"Total number of values in the DataFrame:{df.shape[0]}")

                print(df.head(3))

                # 1. Identify duplicate values based on 'STATION_ID' and 'DATE'
                duplicate_station_ids = df[df['RECORD_ID'].duplicated(keep=False)]

                # 2. Display the rows with duplicate 'STATION_ID' and 'DATE'
                print(f"Rows with duplicate STATION_ID and DATE:{len(duplicate_station_ids)}")

                # df.to_excel("output.xlsx")

                return df
            except Exception as e:
                print("Error message: ", e)
        else:
            print(f"Failed to retrieve the file list. Status code: {response.status_code}")


    except Exception as e:
        print(e)


def insert_data(get_data):

    try:
        global conn
        conn = sqlite3.connect('CortevaDB.db')
        #print(get_data)


        print("Total number of values in the DataFrame:", get_data.shape[0])
        logging.info(f"Total number of values in the DataFrame:{get_data.shape[0]}")

        for index, row in get_data.iterrows():
            # Prepare data for insertion
            row_data = (row['RECORD_ID'],row['STATION_ID'], row['DATE'], row['MAX_TEMP'], row['MIN_TEMP'], row['TOTAL_PRECIPITATION'])


            # Check if the data already exists
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT COUNT(*) FROM Weather_data
                        WHERE RECORD_ID = ? 
                    ''', row_data)

            exists = cursor.fetchone()[0]

            if exists == 0:
            # Insert the new record if it does not exist
                cursor.execute('''
                                INSERT INTO Weather_data (STATION_ID, DATE, MAX_TEMP, MIN_TEMP, TOTAL_PRECIPITATION)
                                VALUES (?, ?, ?, ?, ?)
                            ''', row_data)

            # Commit the changes
        conn.commit()
        print("Data has been Inserted to the DB")

    except Exception as e:
        print(e)

def Onetime_insert_data(get_data):
    try:
        print("inside insert function")


        # Connect to the SQLite database (it will create one if not existing)
        conn = sqlite3.connect('CortevaDB.db')

        # Insert the DataFrame into the SQLite table 'weather_data'
        get_data.to_sql('Weather_Data', conn, if_exists='append', index=False)

        # Close the connection
        conn.close()
        print("One time process Insert has been successfully completed")

    except Exception as e:
        print(e)


def main():
    try:
        global conn
        #================= START LOG FILE=======================================
        logging.basicConfig(filename='ingestion_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

        # Log the start time
        start_time = datetime.now()
        logging.info(f"Data ingestion started at {start_time}")

        #====================READ DATA==========================
        get_data=data_process(api_url,username,token)

        #This below function is used to insert the data one time process only.
        #Onetime_insert_data(get_data)

        # This below function is used to insert the data on daily basis if we recieve
        # a new data it will insert and it won't insert the duplicate one. To insert on a daily basis we can schedule
        # the script in task scheduler.

        insert_data(get_data)
        #print(get_data)

        end_time = datetime.now()
        logging.info(f"Data ingestion completed at {end_time}")

        #=================END LOG FILE=======================================


    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)


if __name__=='__main__':
    main()
