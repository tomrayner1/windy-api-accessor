import requests


def main():
  data = {
    "lat": 0,
    "lon": 0,
    "model": "gfs",
    "parameters": ["temp"],
    "key": "",
  }

  response = requests.post("https://api.windy.com/api/point-forecast/v2", json=data)

  print(f"windy says {response.status_code}: {response.text}")

  return


if __name__ == "__main__":
  main()