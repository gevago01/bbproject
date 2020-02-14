import concurrent.futures
from datetime import datetime
import re
import logging
import requests, random

import time

fileName = "experiments/benchmarkSameChunk.txt"
container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain"
nofRetrievals = 100
times = []

"""checks if dimensions of object are 64x64x64
    if not, a random object is selected anew
"""


def valid_object(randomObject):
    # remove the name
    objectWoName = re.sub(r'.*/', '', randomObject)
    dimensions = objectWoName.split("_")
    for dim_i in dimensions:
        intervals = dim_i.split("-");
        if (int(intervals[1]) - int(intervals[0])) != 64:
            return False

    return True


def get_all_objects():
    all_objects = requests.get(container, params=None)
    return all_objects.text.splitlines()


def thread_function(name):
    logging.info("Thread %s: starting", name)
    with requests.Session() as session:
        for i in range(0, nofRetrievals):
            start = time.time()
            request_object(random_object, session)
            end = time.time()
            times.append(end - start)
    logging.info("Thread %s: finishing", name)


def request_object(object, session):
    session.get(container + "/" + object)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"

    all_objects = get_all_objects()

    random_object = random.choice(all_objects)
    print(random_object)

    while not valid_object(random_object):
        random_object = random.choice(all_objects)

    print(random_object)

    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

    with open(fileName, 'a') as f:
        f.write("#%s\n" % datetime.now())
        for retTime in times:
            f.write("%s\n" % retTime)
