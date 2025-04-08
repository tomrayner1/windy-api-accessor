import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import os
from src.database.database import get_session
from src.database.models import TemperatureData
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


MYT = timezone(timedelta(hours=8))

def group_by_day(times):
    """
    Sorts a dictionary of {<timestamp>: <temperature>} into a list of [{<timestamp>: [<temperature ...>, ]}]
    """
    grouped = defaultdict(list)

    for timestamp, temp in times.items():
        date_str = datetime.fromtimestamp(timestamp, MYT).strftime('%Y-%m-%d')
        grouped[date_str].append(temp)

    return grouped


def insert_file(files):
    """
    Loops through each file provided and then inserts the data from weather_data/
    """
    for file_name in files:
        #
        file = f"weather_data/{file_name}"

        # Load JSON into memory
        with open(file, "r") as datafile:
            data = json.load(datafile)

        # Loop through every coordinate in the JSON
        for key in data:
            coords = key.split(", ")
            lat = float(coords[0])
            long = float(coords[1])

            print(f"\nlat: {lat} long: {long}")

            times = {}

            # Loop through each timestamp and group it with its 
            for ts, kelvin in zip(data[key]["ts"], data[key]["temp-surface"]):
                # Convertions
                seconds_epoch = int(ts / 1000)
                celsius = kelvin - 273.15
                times[seconds_epoch] = celsius

            # Group timestamps and temperatures by new days in Malaysia
            daily_groups = group_by_day(times)

            # Loop through each day
            for date in sorted(daily_groups):
                day_temps = daily_groups[date]
                # Calculate stats
                min_temp = min(day_temps)
                max_temp = max(day_temps)
                avg_temp = sum(day_temps) / len(day_temps)

                print(f"{date} - min: {min_temp:.2f}°C, max: {max_temp:.2f}°C, avg: {avg_temp:.2f}°C")

                # Query if data already exists in the database
                existing = db_session.query(TemperatureData).filter_by(
                    Source_Name="Windy",
                    Date=date,
                    Latitude=lat,
                    Longitude=long
                ).first()

                # If the data exists, skip
                if existing:
                    print(f"Skipping duplicate entry for {date} @ ({lat}, {long})")
                    continue

                # Create new record for the day
                try:
                    new_record = TemperatureData(
                        Source_Name="Windy",
                        Date=date,
                        Latitude=lat,
                        Longitude=long,
                        Min_Temp=min_temp,
                        Max_Temp=max_temp,
                        Avg_Temp=avg_temp,
                    )
                    db_session.add(new_record)

                except IntegrityError:
                    db_session.rollback()
                except SQLAlchemyError:
                    db_session.rollback()
                except Exception:
                    db_session.rollback()



if __name__ == "__main__":
    db_session = get_session()

    files = os.listdir("weather_data")

    files.remove("old_data")
    files.remove(".git")
    files.remove("README.md")
    
    insert_file(files)

    db_session.commit()

    db_session.close()