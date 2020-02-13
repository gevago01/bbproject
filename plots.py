import sys
import numpy as np
import matplotlib.pyplot as plt


def plotTime(times, input_file):
    timeMean = np.mean(times)
    timesStd = np.std(times)
    # Build the plot
    fig, ax = plt.subplots()
    barLabels = ['']
    x_pos = np.arange(len(barLabels))
    avgTime = [timeMean]
    error = [timesStd]
    ax.bar(x_pos, avgTime, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
    # ax.set_ylabel('')
    ax.margins(0.1, 0.1)
    ax.set_ylabel('Average Retrieval Time (seconds)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(barLabels)
    ax.set_title('Average Retrieval Time for Same 64x64x64 Chunk')
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()

    output_file = input_file.split("/")[1]
    plt.savefig('plots/' + output_file + '.png')
    plt.show()


def main():
    fileName = sys.argv[1]
    timeMesaurements = []
    with open(fileName) as f:
        for l in f:
            if not l.startswith("#"):
                timeMesaurements.append(l)

    timesM = np.array(timeMesaurements).astype(np.double)

    plotTime(timesM, sys.argv[1])


if __name__ == '__main__':
    main()
