import datetime
import json
from src.coordinates import *


def testmain():
    print(f"{datetime.datetime.today().strftime("%d_%B_%H%M")}.json")

    coordinates = load_coordinates()

    print(f"{coordinates}\n\nLooping through coordinates...")

    for coordinate in coordinates:
        print(f"lat: {coordinate[0]}, long: {coordinate[1]}")

    datastr = ""
    filename = "test.json"

    with open(filename, 'r') as file:
        datastr = file.read().rstrip('\n')

    newstr = datastr[:-2]
    newstr += "}"

    newstr = newstr.replace(',"warning":"The trial API version is for development purposes only. This data is randomly shuffled and slightly modified."', '')

    jsondata = json.loads(newstr)

    with open(filename, 'w+') as file:
        file.truncate(0)
        file.write(json.dumps(jsondata, indent=2))

    return


if __name__ == "__main__":
    testmain()