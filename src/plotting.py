import os
import yaml
import numpy
import matplotlib.pyplot as plt

PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
DATA_DIR = os.path.join(PATH, "data")


def getDataFiles(keyword="results_"):
    files = os.listdir(DATA_DIR)
    files = [file for file in files if keyword in file]  # Python moment
    files.sort()
    return files


def loadFile(file_name):
    path = os.path.join(DATA_DIR, file_name)
    file = open(path)
    data = yaml.safe_load(file)
    file.close()

    return data


def getDataTypes():
    files = getDataFiles()
    data = loadFile(files[0])
    data_types = list(data["ants"][0].keys())
    return data_types


def loadResults():
    """
    :returns {field_name: array[generation][colony_id], ...}
    """

    files = getDataFiles()
    fields = getDataTypes()

    data = {}

    for file_name in files:
        single_file_data_dict = {}

        file_data = loadFile(file_name)["ants"]
        for colony in file_data:
            for field in fields:
                if field not in single_file_data_dict:
                    single_file_data_dict[field] = []

                single_file_data_dict[field].append(colony[field])

        for field in single_file_data_dict:
            data_arr = numpy.expand_dims(numpy.asarray(single_file_data_dict[field]), 0)
            if field not in data:
                data[field] = data_arr
            else:
                data[field] = numpy.append(data[field], data_arr, 0)

    return data


def singleVariableAxis(data_mat, ax, color=None, show_error_bars=False):
    x = []
    y = []
    min_val = []
    max_val = []
    for generation in range(data_mat.shape[0]):
        gen_data = data_mat[generation]
        mean = numpy.mean(gen_data)

        x.append(generation)
        y.append(mean)
        min_val.append(abs(mean - min(gen_data)))
        max_val.append(abs(mean - max(gen_data)))

    error_bars = [min_val, max_val]

    if show_error_bars:
        return ax.errorbar(x, y, yerr=error_bars, color=color)
    else:
        return ax.plot(x, y, color=color)


def plotAllVariables(data):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    a = singleVariableAxis(data["population"], ax1, color="red")

    b = singleVariableAxis(data["size"], ax2)
    c = singleVariableAxis(data["spawn_interval"], ax2)
    d = singleVariableAxis(data["speed"], ax2)
    lns = a + b + c + d

    plt.title("Ant evolution")
    ax1.set_xlabel("Generations")
    ax1.set_ylabel("Population")
    ax2.set_ylabel("Parameter value")

    ax1.legend(lns, ["Population", "Size", "Spawn interval", "Speed"], loc=9)

    # plt.show()
    plt.savefig("all_data.png")


def plotSingleVariable(data, field):
    fig, ax1 = plt.subplots()
    singleVariableAxis(data[field], ax1, color="red")
    plt.show()


def main():
    data = loadResults()
    # plotSingleVariable(data, "speed")
    plotAllVariables(data)


if __name__ == '__main__':
    main()
