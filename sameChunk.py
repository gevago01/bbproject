import requests
import random
import time
import numpy as np
import matplotlib.pyplot as plt

container = "https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain"
nofRetrievals = 20


def getAllObjects():
    allObjects = requests.get(container, params=None)
    return allObjects.text.splitlines()


def getObject(object):
    requests.get(container+"/"+object, params=None)


def plotTime(timeMean, timesStd):
    # Build the plot
    fig, ax = plt.subplots()
    barLabels = ['']
    x_pos = np.arange(len(barLabels))
    CTEs = [timeMean]
    error = [timesStd]
    ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
    # ax.set_ylabel('')
    ax.set_ylabel('Average Retrieval Time (seconds)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(barLabels)
    ax.set_title('Average Retrieval Time for Same 64x64x64 Chunk')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig('bar_plot_with_error_bars.png')
    plt.show()


def main():
    print("running..")

    allObjects = getAllObjects()

    randomObject = random.choice(allObjects)
    print(randomObject)

    times = []
    for i in range(0, nofRetrievals):
        start = time.time()
        getObject(randomObject)
        end = time.time()
        times.append(end-start)


    timeMean = np.mean(times)
    timesStd = np.std(times)
    plotTime(timeMean, timesStd)




if __name__ == '__main__':
    main()