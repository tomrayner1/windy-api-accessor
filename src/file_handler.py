import os 

def create_folder():
  """
  Creates the weather data folder if it doesn't exist already
  """
  if not os.path.exists("weather_data"):
    os.makedirs("weather_data")
