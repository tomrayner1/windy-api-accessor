def load_keys():
  """
  Loads the API keys from keys.txt in the project's root.
  """
  keys = []

  with open("keys.txt") as keyfile:
    for line in keyfile:
      keys.append(line.replace('\n', ''))
  
  return keys