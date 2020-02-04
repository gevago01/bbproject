from datetime import datetime
import requests
import random
import time
import re


fileName = "experiments/benchmarkRandomChunks.txt"
container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain"
nofRetrievals = 100


def getAllObjects():
    allObjects = requests.get(container, params=None)
    return allObjects.text.splitlines()


def requestObject(object):
    requests.get(container + "/" + object, params=None)


"""checks if dimensions of object are 64x64x64
    if not, a random object is selected anew
"""
def validObject(randomObject):
    # remove the name
    objectWoName = re.sub(r'.*/', '', randomObject)
    dimensions = objectWoName.split("_")
    for dim_i in dimensions:
        intervals = dim_i.split("-");
        if (int(intervals[1]) - int(intervals[0])) != 64:
            return False

    return True

def getRanObject(allObjects):
    randomObject = random.choice(allObjects)

    while not validObject(randomObject):
        randomObject = random.choice(allObjects)

    return randomObject


def main():
    print("running..")

    allObjects = getAllObjects()

    times = []
    for i in range(0, nofRetrievals):
        randomObject = getRanObject(allObjects)
        start = time.time()
        requestObject(randomObject)
        end = time.time()
        times.append(end - start)

    with open(fileName, 'a') as f:
        f.write("#%s\n" % datetime.now())
        for retTime in times:
            f.write("%s\n" % retTime)


if __name__ == '__main__':
    main()
