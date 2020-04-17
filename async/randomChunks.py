from datetime import datetime

import aiohttp
import random
import asyncio
import time
import logging
import csv
import re

filename = "experiments/benchmarkRandomChunks.txt"
swift_container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain/"
dvid_container = "http://148.187.97.94:8000/api/node/8f/grayscale/raw/0_1_2/64_64_64/"
nof_retrievals = 100
MAX_CONNECTIONS = 8
dvid_times = []
swift_times = []


async def get_all_objects(session):
    async with session.get(swift_container) as resp:
        return await resp.text()


"""checks if dimensions of object are 64x64x64
    if not, a random object is selected anew
"""


def valid_object(random_object):
    # remove the name
    object_wo_name = re.sub(r'.*/', '', random_object)
    dimensions = object_wo_name.split("_")
    for dim_i in dimensions:
        intervals = dim_i.split("-");
        if (int(intervals[1]) - int(intervals[0])) != 64:
            return False

    return True


''' Returns one random object
'''


def get_ran_object(allObjects):
    random_object = random.choice(allObjects)

    while not valid_object(random_object):
        random_object = random.choice(allObjects)

    return random_object


async def swift_retrieve(random_object, session):
    start = time.perf_counter()
    response = await session.get(swift_container + random_object)
    end = time.perf_counter()  # Mark the end of request before the read
    await response.read()
    swift_times.append(end - start)

async def dvid_retrieve(random_object, session):
    #remove swift id
    object_wo_id = re.sub(r'.*/', '', random_object)
    split_point = object_wo_id.split("_")
    starting_offsets = [interval.split("-")[0] for interval in split_point]
    start = time.perf_counter()
    response = await session.get(dvid_container + starting_offsets[0]+"_"+starting_offsets[1]+"_"+starting_offsets[2])
    end = time.perf_counter()  # Mark the end of request before the read
    await response.read()
    dvid_times.append(end - start)


# def init_session(connections):
#     tcp_connector = aiohttp.TCPConnector(limit=connections)
#     session = aiohttp.ClientSession(connector=tcp_connector)
#     return session


async def close_sessions(session):
    await session.close()


def write_to_file():
    with open(filename, 'a') as f:
        csv_writer = csv.writer(f, delimiter="\t")
        f.write("#%s\n" % datetime.now())
        f.write("#swift\tdvid\n" )
        csv_writer.writerows(zip(swift_times, dvid_times))
        # f.write("#%s\n" % datetime.now())
        # for i in range(0, len(times[0])):
        #     f.write("%s\t%s\n" % times[0][i], times[1][i])


def swift_experiments():
    print("running..")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    tcp_connector = aiohttp.TCPConnector(limit=MAX_CONNECTIONS)
    session = aiohttp.ClientSession(connector=tcp_connector)
    loop = session.connector._loop

    task = [get_all_objects(session)]

    all_objects = loop.run_until_complete(
        asyncio.gather(*task)
    )
    all_objects = all_objects[0].splitlines()

    random_objects = []
    # fill the list with random objects
    for i in range(0, nof_retrievals):
        random_objects.append(get_ran_object(all_objects))

    task = [swift_retrieve(ran_object, session)
            for ran_object in random_objects]

    loop.run_until_complete(
        asyncio.wait(task)
    )

    loop.run_until_complete(asyncio.wait_for(close_sessions(session), None))


    return random_objects

async def initialize_dvid_session(session):
    # request object at 0, 0, 0 to initialize the session
    async with session.get(dvid_container + "0_0_0") as resp:
        return await resp.text()


def dvid_experiments(random_objects):
    tcp_connector = aiohttp.TCPConnector(limit=MAX_CONNECTIONS)
    session = aiohttp.ClientSession(connector=tcp_connector)
    loop = session.connector._loop

    task = [initialize_dvid_session(session)]

    loop.run_until_complete(
        asyncio.gather(*task)
    )

    task = [dvid_retrieve(ran_object, session)
            for ran_object in random_objects]

    loop.run_until_complete(
        asyncio.wait(task)
    )

    loop.run_until_complete(asyncio.wait_for(close_sessions(session), None))


def main():
    objects = swift_experiments()
    dvid_experiments(objects)

    write_to_file()


if __name__ == '__main__':
    main()
