import asyncio
import concurrent
import concurrent.futures
from datetime import datetime

import aiohttp
import requests
import random
import asyncio
import time
import logging
import re

filename = "experiments/benchmarkRandomChunks.txt"
container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain/"
nof_retrievals = 100
MAX_CONNECTIONS = 3
times = []


def get_all_objects():
    all_objects = requests.get(container, params=None)
    return all_objects.text.splitlines()

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

''' Returns one random object
'''
def get_ran_object(allObjects):
    random_object = random.choice(allObjects)

    while not valid_object(random_object):
        random_object = random.choice(allObjects)

    return random_object


async def thread_function(random_object, session):
    start = time.perf_counter()
    response = await session.get(container+random_object)
    # print(response.status)
    end = time.perf_counter()  # Mark the end of request before the read
    await response.read()
    times.append(end - start)

    # logging.info("Thread %s: finishing", name)

def init_session(connections):
    tcp_connector = aiohttp.TCPConnector(limit=connections)
    session = aiohttp.ClientSession(connector=tcp_connector)
    return session


async def close_sessions(session):
    await session.close()


def main():
    print("running..")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")


    all_objects = get_all_objects()
    random_objects = []
    #fill the list with random objects
    for i in range(0, nof_retrievals):
        random_objects.append(get_ran_object(all_objects))


    tcp_connector = aiohttp.TCPConnector(limit=MAX_CONNECTIONS)
    session = aiohttp.ClientSession(connector=tcp_connector)
    loop = session.connector._loop


    # loop.run_until_complete(asyncio.wait_for(init_sessions(loop, connections), None))
    # session = init_session(loop, 3)

    task = [thread_function(ran_object, session)
                  for ran_object in random_objects]

    loop.run_until_complete(
        asyncio.wait(task)
    )

    loop.run_until_complete(asyncio.wait_for(close_sessions(session), None))
    with open(filename, 'a') as f:
        f.write("#%s\n" % datetime.now())
        for retTime in times:
            f.write("%s\n" % retTime)


if __name__ == '__main__':
    main()
