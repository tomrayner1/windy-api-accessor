import requests
import datetime
import time
import json
from src.key_loader import *
from src.file_handler import *
from src.coordinates import *
from src.database.database import get_session
from src.database.models import TemperatureData
from src.new_insert2 import group_by_day


def main():
  print(f"Running now (at {datetime.datetime.today().strftime("%d_%B_%H%M")})")

  # Start timing 
  start = time.perf_counter()

  # Load all API keys from keys.txt
  keys = load_keys()
  print(f"Loaded {len(keys)} api keys")

  # Create weather_data folder
  create_folder()

  # Error if we got no keys.
  if keys == 0:
    print("Could not load any windy api keys from keys.txt")
    return

  # Load coordinates from coordinates.txt
  coords = load_coordinates()
  print(f"Loaded {len(coords)} coordinates.")

  # Format name for file
  filename = f"weather_data/{datetime.datetime.today().strftime("%d_%B_%H%M")}.json"

  attempts = 0
  errors = 0

  print(f"Requesting data from API endpoint")

  # Open data file
  with open(filename, 'a') as file:
    # Write json
    file.write('{\n')

    # Loop through each coordinate
    for coord in coords:
      attempts += 1

      # Get the lat & long
      x = coord[0] # Latitude
      y = coord[1] # Longitude

      # Construct request body
      data = {
        "lat": f"{x}",
        "lon": f"{y}",
        "model": "gfs",
        "parameters": ["temp", "ptype", "precip", "wind", "windGust", "lclouds", "mclouds", "hclouds"],
        "levels": ["surface"],
        "key": f"{keys[0]}"
      }

      # Send request
      response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)
      # Request code
      # print(f"windy says {response.status_code}.")

      # Good response, write data to file
      if response.status_code == 200:
        file.write(f'  "{x}, {y}": {response.text},')
      # API key could've reached limit
      else:
        print(f"ERROR: {response.text}")

        attempts += 1

        # Delete the current key and retry with the next one
        del keys[0]
        print(f"Retrying...")

        # Construct request body
        data = {
          "lat": f"{x}",
          "lon": f"{y}",
          "model": "gfs",
          "parameters": ["temp", "ptype", "precip", "wind", "windGust", "lclouds", "mclouds", "hclouds"],
          "levels": ["surface"],
          "key": f"{keys[0]}"
        }

        # Send request
        response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)
        # Request code
        print(f"retry: {response.status_code}.")

        # Good response, write data to file
        if response.status_code == 200:
          file.write(f'  "{x}, {y}": {response.text},')
        # Not an API key issue, something has actually gone wrong
        else:
          print(f"Retry failed.\nREASON: {response.text}")

          errors += 1

    file.write('}\n')

  print(f"API calls: {attempts}, Errors: {errors}")

  # Formatting JSON
  rawdata = ""

  # Read file data to string
  with open(filename, 'r') as file:
    rawdata = file.read().rstrip('\n')
  
  # Make parsable JSON
  rawdata = rawdata[:-2]
  rawdata += "}"
  # Remove warning
  rawdata = rawdata.replace(',"warning":"The testing API version is for development purposes only. This data is randomly shuffled and slightly modified."', '')

  # Convert string to JSON
  jsondata = json.loads(rawdata)

  # Dump JSON to file
  with open(filename, 'w+') as file:
    file.truncate(0)
    file.write(json.dumps(jsondata, indent=2))
  
  print(f"Wrote data to {filename}")

  # Re-open the file we just saved, attempt to save it to the database,
  # if it fails we still have the backup file.
  try:
    print("Attempting to insert/update ~5000 database entries, this will take a while")
    db_session = get_session()

    with open(filename, 'r') as file:
      data = json.load(file)
    
    for key in data:
      coords = key.split(", ")
      lat = float(coords[0])
      long = float(coords[1])

      times = {}

      for ts, kelvin in zip(data[key]["ts"], data[key]["temp-surface"]):
        seconds_epoch = int(ts / 1000)
        celsius = kelvin - 273.15
        times[seconds_epoch] = celsius

        daily_groups = group_by_day(times)

        for date in sorted(daily_groups):
          day_temps = daily_groups[date]
          min_temp = min(day_temps)
          max_temp = max(day_temps)
          avg_temp = sum(day_temps) / len(day_temps)

          existing = db_session.query(TemperatureData).filter_by(
            Source_Name="Windy",
            Date=date,
            Latitude=lat,
            Longitude=long
          ).first()

          if existing:
            continue

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
          except Exception:
            db_session.rollback()
  # Catch any errors during SQL
  except Exception as e:
    print(f"Failed to update database.\n{e}")
  # Try to commit and close any changes that were made before errors
  finally:
    try:
      db_session.commit()
      db_session.close()

      print(f"Updated database with new data, {filename} can be deleted.")
    except Exception as _:
      print()

  # Time how long we took
  end = time.perf_counter()
  print(f"Finished in {(end - start):.2f}s.\n")

  return


if __name__ == "__main__":
  main()