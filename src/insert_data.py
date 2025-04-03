import json
from datetime import datetime
import os
from database.database import get_session
from database.models import TemperatureData
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


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

TEST_FILE = "weather_data/13_March_1008.json"


def insert_data(file_name: str):
    
    file = f"weather_data/{file_name}"

    db_session = get_session()

    with open(file, "r") as datafile:
        data = json.load(datafile)

    for key, _ in data.items():
        coords = key.split(", ")
        lat = float(coords[0])
        long = float(coords[1])
        

        print(f"\n{lat}, {long}\n" + "-" * 95)

        min_temp = float("inf")
        max_temp = float("-inf")

        for ts, kelvin in zip(data[key]["ts"], data[key]["temp-surface"]):
            seconds_epoch = ts / 1000
            timestamp = datetime.fromtimestamp(seconds_epoch)
            formatted_time = timestamp.strftime("%Y-%m-%d")

            temp = kelvin - 273.15

            min_temp = min(min_temp, temp)
            max_temp = max(max_temp, temp)
            avg_temp = (min_temp + max_temp) / 2


            try:
                new_record = TemperatureData(
                    Source_Name="Windy",
                    Date=formatted_time,
                    Latitude=lat,
                    Longitude=long,
                    Min_Temp=min_temp,
                    Max_Temp=max_temp,
                    Avg_Temp=avg_temp,
                )
                db_session.add(new_record)
                db_session.commit()
            except IntegrityError as e:
                db_session.rollback()
                print(f"Duplicated data... skipping")
            except SQLAlchemyError as e:
                db_session.rollback()
                print(f"Error inserting data: {e}")

            except Exception as e:
                db_session.rollback()
                print(f"Error inserting data: {e}")

        db_session.close()
        print("Finished inserting data. Closing session.")

    return

# get files in weather data

files = os.listdir("weather_data")

files.remove("old_data")
files.remove(".git")
files.remove("README.md")

print(files)

for file in files:
    insert_data(file_name=file)

