import datetime
from src.coordinates import *


def testmain():
    print(f"{datetime.datetime.today().strftime("%d_%B_%H%M")}.json")

    coordinates = load_coordinates()

    print(f"{coordinates}\n\nLooping through coordinates...")

    for coordinate in coordinates:
        print(f"lat: {coordinate[0]}, long: {coordinate[1]}")

    return


if __name__ == "__main__":
    testmain()