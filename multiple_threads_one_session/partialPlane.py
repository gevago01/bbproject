from datetime import datetime
import concurrent.futures
import logging
import requests
import random
import time
import re

fileName = "experiments/benchmarkPartialPlane.txt"
container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain"
nofRetrievals = 100
times = []


def get_all_objects():
    allObjects = requests.get(container, params=None)
    return allObjects.text.splitlines()


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
        intervals = dim_i.split("-")
        if (int(intervals[1]) - int(intervals[0])) != 64:
            return False

    return True


def get_ran_object(allObjects):
    random_object = random.choice(allObjects)
    print(random_object)

    while not valid_object(random_object):
        random_object = random.choice(allObjects)

    print(random_object)

    return random_object


def find_max_y_z_coors(fixed_x_coordinate):
    max_y = -1
    max_z = -1

    for point in fixed_x_coordinate:
        split_point = point.split("_")
        y_coordinates = split_point[1]
        y_range = y_coordinates.split("-")
        z_coordinates = split_point[2]
        z_range = z_coordinates.split("-")

        # second number in the range is always bigger
        if int(y_range[1]) > max_y:
            max_y = int(y_range[1])

        if int(z_range[1]) > max_z:
            max_z = int(z_range[1])

    return max_y, max_z


def find_partial_plane(fixed_x_coordinate, max_y, max_z):
    partial_plane_max_y = max_y / 4
    partial_plane_max_z = max_z / 4
    partial_plane_points = []
    for point in fixed_x_coordinate:
        split_point = point.split("_")
        y_coordinates = split_point[1]
        y_range = y_coordinates.split("-")
        z_coordinates = split_point[2]
        z_range = z_coordinates.split("-")

        if int(y_range[1]) <= partial_plane_max_y and int(z_range[1]) <= partial_plane_max_z:
            partial_plane_points.append(point)

    return partial_plane_points


def thread_function(name):
    logging.info("Thread %s: starting", name)
    all_objects = get_all_objects()

    random_object = get_ran_object(all_objects)
    objects_starting_with = random_object.split("_")[0]

    fixed_x_coordinate = [o for o in all_objects if o.startswith(objects_starting_with)]

    max_y, max_z = find_max_y_z_coors(fixed_x_coordinate)

    partial_plane_points = find_partial_plane(fixed_x_coordinate, max_y, max_z)

    print("partial_plane_points:", len(partial_plane_points))

    with requests.Session() as session:
        for partial_plane_object in partial_plane_points:
            start = time.time()
            request_object(partial_plane_object, session)
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

    with open(fileName, 'a') as f:
        f.write("#%s\n" % datetime.now())
        for retTime in times:
            f.write("%s\n" % retTime)


if __name__ == '__main__':
    main()
