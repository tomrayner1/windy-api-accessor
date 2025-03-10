import requests
import time
from src.key_loader import *
from src.file_handler import *

#TOP_LEFT = (5.49, 100.17)
#BOTTOM_RIGHT = (5.26, 100.34)

def main():
  print("-"*80 + "\nWindy API Accessor\n" + "-"*80)

  # Start timing 
  start = time.perf_counter()
  # Load all API keys from keys.txt
  keys = load_keys()

  create_folder()

  # Error if we got no keys.
  if keys == 0:
    print("Could not load any windy api keys from keys.txt.")
    return

  i = 0

  with open('weather_data/test.json', 'a') as file:
    file.write('{\n')
    for xLoop in range(49, 26-1, -1):
      for yLoop in range(17, 34+1):
        x = 5 + (xLoop / 100)
        y = 100 + (yLoop / 100)

        data = {
          "lat": x,
          "lon": y,
          "model": "gfs",
          "parameters": ["temp"],
          "key": "",
        }

        response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)

        print(f"windy says {response.status_code}.")

        if response.status_code == 200:
          file.write(f'  "{x}, {y}": {response.text},')
        else:
          print(f"ERROR: {response.text}")
        i += 1

    file.write('}\n')
  
  print(f"{i} positions checked.")

  

  

  # Time how long we took
  end = time.perf_counter()
  print(f"Finished in {end - start}s.")

  return


if __name__ == "__main__":
  main()