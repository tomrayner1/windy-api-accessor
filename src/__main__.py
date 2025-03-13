import requests
import datetime
import time
from src.key_loader import *
from src.file_handler import *
from src.coordinates import *


def main():
  print("-"*80 + "\nWindy API Accessor\n" + "-"*80)

  # Start timing 
  start = time.perf_counter()

  # Load all API keys from keys.txt
  keys = load_keys()
  print(f"Loaded {len(keys)} api keys.")

  # Create weather_data folder
  create_folder()

  # Error if we got no keys.
  if keys == 0:
    print("Could not load any windy api keys from keys.txt.")
    return

  # Load coordinates from coordinates.txt
  coords = load_coordinates()
  print(f"Loaded {len(coords)} coordinates.")

  # Format name for file
  filename = f"weather_data/{datetime.datetime.today().strftime("%d_%B_%H%M")}.json"

  # Open data file
  with open(filename, 'a') as file:
    # Write json
    file.write('{\n')

    # Loop through each coordinate
    for coord in coords:
      # Get the lat & long
      x = coord[0] # Latitude
      y = coord[1] # Longitude

      # Construct request body
      data = {
        "lat": x,
        "lon": y,
        "model": "gfs",
        "parameters": ["temp", "ptype", "precip", "wind", "windGust", "lclouds", "mclouds", "hclouds"],
        "key": keys[0],
      }

      # Send request
      response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)
      # Request code
      print(f"windy says {response.status_code}.")

      # Good response, write data to file
      if response.status_code == 200:
        file.write(f'  "{x}, {y}": {response.text},')
      # API key could've reached limit
      else:
        print(f"ERROR: {response.text}")
        # Delete the current key and retry with the next one
        del keys[0]
        print(f"Retrying...")

        # Construct request body
        data = {
          "lat": x,
          "lon": y,
          "model": "gfs",
          "parameters": ["temp", "ptype", "precip", "wind", "windGust", "lclouds", "mclouds", "hclouds"],
          "key": keys[0],
       }

        # Send request
        response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)
        # Request code
        print(f"windy says {response.status_code}.")

        # Good response, write data to file
        if response.status_code == 200:
          file.write(f'  "{x}, {y}": {response.text},')
        # Not an API key issue, something has actually gone wrong
        else:
          print(f"Retry failed.\nREASON: {response.text}")

    file.write('}\n')
  
  # Time how long we took
  end = time.perf_counter()
  print(f"Finished in {end - start}s.")

  return


if __name__ == "__main__":
  main()