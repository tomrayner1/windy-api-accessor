import os 

def create_folder():
  if not os.path.exists("weather_data"):
    os.makedirs("weather_data")
