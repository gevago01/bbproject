from datetime import datetime
import requests
import random
import time
import re

file_name = "experiments/benchmarkSameChunk.txt"
container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain"
nof_retrievals = 100


def get_all_objects():
    all_objects = requests.get(container, params=None)
    return all_objects.text.splitlines()


def request_object(object, session):
    session.get(container + "/" + object)


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


def main():
    print("running..")

    all_objects = get_all_objects()

    random_object = random.choice(all_objects)
    print(random_object)

    while not valid_object(random_object):
        random_object = random.choice(all_objects)

    print(random_object)

    times = []
    with requests.Session() as session:
        for i in range(0, nof_retrievals):
            start = time.time()
            request_object(random_object, session)
            end = time.time()
            times.append(end - start)

    with open(file_name, 'a') as f:
        f.write("#%s\n" % datetime.now())
        for retTime in times:
            f.write("%s\n" % retTime)


if __name__ == '__main__':
    main()
