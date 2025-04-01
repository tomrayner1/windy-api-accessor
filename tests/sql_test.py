import mysql.connector
import json
from datetime import datetime
from src.coordinates import *

# Temperature_Data & Temperature_Data_Test columns
"""
('Temperature_ID',)
('Source_Name',)
('Date',)
('Latitude',)
('Longitude',)
('Min_Temp',)
('Max_Temp',)
('Avg_Temp',)
"""

EXECUTE_SQL = True
TEST_FILE = "weather_data/13_March_1008.json"
SQL = """
SELECT *
FROM Temperature_Data_Test;
"""


def sql_test():
  connection_details = []

  with open("database_creds.txt", 'r') as credsfile:
    for line in credsfile:
      connection_details.append(line.replace('\n', ''))

  conn = mysql.connector.connect(
    host=f"{connection_details[0]}",
    user=f"{connection_details[2]}",
    password=f"{connection_details[4]}",
    database=f"{connection_details[3]}",
    port=connection_details[1]
  )

  cursor = conn.cursor()

  with open(TEST_FILE, 'r') as datafile:
    data = json.load(datafile)
  
  for key, _ in data.items():
    coords = key.split(', ')

    lat = coords[0]
    long = coords[1]

    print(f"\n{lat}, {long}\n-----------------------------------------------------------------------------------------------")

    min = 9999
    max = 0

    for ts, kelvin in zip(data[key]["ts"], data[key]["temp-surface"]):
      seconds_epoch = ts / 1000
      timestamp = datetime.fromtimestamp(seconds_epoch)
      formatted_time = timestamp.strftime('%Y-%m-%d')

      temp = kelvin - 273.15

      print(formatted_time)
      break

      if temp > max:
        max = temp
      
      if temp < min:
        min = temp

      if True:
        sql = f"""
INSERT INTO Temperature_Data_Test (Source_Name, Date, Latitude, Longitude, Min_Temp, Max_Temp, Avg_Temp)
VALUES ('Windy', {formatted_time}, {lat}, {long}, {min}, {max}, {temp});
"""
        
        if EXECUTE_SQL:
          cursor.execute(sql)
          print(f"Inserted data for {ts}.")
      else:
        #print(f"{formatted_time}: {temp}°C (Min: {min}°C, Max: {max}°C)")
        break

  if False:
    cursor.execute("SELECT * FROM Temperature_Data_Test;")

    for row in cursor:
      print(f"{row}")

  cursor.close()
  conn.close()

  return