import requests
from src.key_loader import *

def request_fix():
  data = {
    "lat": 5.60948,
    "lon": 100.3833,
    "model": "gfs",
    "parameters": ["temp", "ptype", "precip", "wind", "windGust", "lclouds", "mclouds", "hclouds"],
    "levels": ["surface"],
    "key": "-"
  }

  response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)

  print(f"{response.text}")

  print(f"{load_keys()}")

  return