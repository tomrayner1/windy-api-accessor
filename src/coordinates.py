def load_coordinates():
    coords = []

    with open("coordinates.txt", 'r') as file:
        for line in file:
            oneline = line.replace('\n', '')
            coords.append(oneline.split(', '))

    return coords