def load_coordinates():
  """
  Loads the coordinates from the coordinates.txt file in root and loads them into an array
  """
  coords = []

  with open("coordinates.txt", 'r') as file:
    for line in file:
      oneline = line.replace('\n', '')
      coords.append(oneline.split(', '))

  return coords