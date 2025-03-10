def load_keys():
  keys = []

  with open("keys.txt") as keyfile:
    for line in keyfile:
      keys.append(line.replace('\n', ''))
  
  print(f"Loaded {len(keys)} api keys.")

  return keys