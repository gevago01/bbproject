import concurrent
import concurrent.futures
from datetime import datetime
import requests
import random
import time
import logging
import re

filename = "experiments/benchmarkRandomChunks.txt"
container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain"
nof_retrievals = 100
times = []


def get_all_objects():
    all_objects = requests.get(container, params=None)
    return all_objects.text.splitlines()


def request_object(object, session):
    session.get(container + "/" + object, params=None)


"""checks if dimensions of object are 64x64x64
    if not, a random object is selected anew
"""


def valid_object(randomObject):
    # remove the name
    object_wo_name = re.sub(r'.*/', '', randomObject)
    dimensions = object_wo_name.split("_")
    for dim_i in dimensions:
        intervals = dim_i.split("-");
        if (int(intervals[1]) - int(intervals[0])) != 64:
            return False

    return True


def get_ran_object(allObjects):
    random_object = random.choice(allObjects)

    while not valid_object(random_object):
        random_object = random.choice(allObjects)

    return random_object


def thread_function(name):
    all_objects = get_all_objects()
    logging.info("Thread %s: starting", name)
    with requests.Session() as session:
        for i in range(0, nof_retrievals):
            random_object = get_ran_object(all_objects)
            start = time.time()
            request_object(random_object, session)
            end = time.time()
            times.append(end - start)
    logging.info("Thread %s: finishing", name)


def main():
    print("running..")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

    with open(filename, 'a') as f:
        f.write("#%s\n" % datetime.now())
        for retTime in times:
            f.write("%s\n" % retTime)


if __name__ == '__main__':
    main()
