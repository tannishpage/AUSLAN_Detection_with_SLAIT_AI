import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
from detector import check_cmd_arguments

def get_files():
    for i, arg in enumerate(sys.argv[1:]):
        if "--" in arg:
            return sys.argv[1:i+1]
    return sys.argv[1:]


def plotter(files, save, title, xlabel, ylabel, key_to_plot, sep_lr, hide):
    fig = plt.figure(1)
    fig.set_size_inches((19.2, 10.8))
    if sep_lr:
        legend = []
    for file in files:
        data = pd.read_csv(file)
        if sep_lr:
            legend += [file+"_LEFT", file+"_RIGHT"]
            left = data.get("Left Entropy", False)
            right = data.get("Right Entropy", False)
            if type(left) == type(bool()) or type(right) == type(bool()):
                print(f"{file} doesn't contain Left or Right entropy! Quitting")
                print("Please run detector.py with the --average flag")
                exit(1)
            plt.plot(data["Frame Number"], left)
            plt.plot(data["Frame Number"], right)
        else:
            plt.plot(data["Frame Number"], data[key_to_plot])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if sep_lr:
        plt.legend(legend)
    else:
        plt.legend(files)
    if save != False:
        fig.savefig(save, dpi=100)
    if not hide:
        plt.show()

def sub_plotter(files, save, title, xlabel, ylabel, key_to_plot, hide, h, w):
    fig = plt.figure(1)
    fig.set_size_inches((19.2, 10.8))
    plt.title(title)
    for i, file in enumerate(files):
        plt.subplot(h, w, i+1)
        data = pd.read_csv(file)
        plt.plot(data["Frame Number"], data[key_to_plot])
        plt.legend([file])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    if save != False:
        fig.savefig(save, dpi=100)
    if not hide:
        plt.show()

def seps_plotter_single_file(file, save, title, xlabel, ylabel, key_to_plot, hide, seps):
    data = pd.read_csv(file)
    step_size = int(seps[-1])
    print("Step Size:", step_size)
    fig = plt.figure(1)
    fig.set_size_inches((19.2, 10.8))
    start = 0
    start_index = 0
    legend = []
    for i, sep in enumerate(seps[:-1]):
        end = start + int(sep)
        end_index = start_index + len(range(start, end, step_size))
        plt.plot(data["Frame Number"][start_index:end_index], data[key_to_plot][start_index:end_index])
        start = range(start, end, step_size)[-1]
        start_index = end_index
        legend.append("Sequence " + str(i))

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    if save != False:
        fig.savefig(save, dpi=100)
    if not hide:
        plt.show()



if __name__ == "__main__":

    USAGE = """Usage: python3 plotter.py <path_to_entropy_csv> [<path_to_entropy_csv>..] [options]

        --help          Display this help message
        --save          Saves plot to specified location
        --hide          doesn't show the plot
        --title         Title of the graph
        --xlabel        Label for x-Axis
        --ylabel        Label for y-Axis
        --sep_lr        Plot left and right hands seperately (Only if --average was used with detector)
        --subplot       Plots all the files in subplots (must pass height and width)
        --EMA           Plots the Entropy's Exponential Moving Average instead (Only if --moving_averages was used with detector)
        --seps          Seperates a sequence and plots them
"""

    if len(sys.argv) < 2:
        print(USAGE)
        exit(1)

    if "--help" == sys.argv[1]:
        print(USAGE)
        exit(1)

    files = get_files()
    if files == None:
        print("No file(s) have been passed, use --help for instructions")
        exit(1)

    save = check_cmd_arguments("--save", "NoPath", False)
    if save == "NoPath":
        print("--save: No path was passed")
        exit(1)

    if save and not os.path.exists(os.path.dirname(save)):
        print("--save: Path does not exist")
        exit(1)

    title = check_cmd_arguments("--title", "", "")
    xlabel = check_cmd_arguments("--xlabel", "", "")
    ylabel = check_cmd_arguments("--ylabel", "", "")
    sep_lr = check_cmd_arguments("--sep_lr", True, False)
    hide = check_cmd_arguments("--hide", True, False)
    subplot = check_cmd_arguments("--subplot", "NoHW", False)
    key_to_plot = check_cmd_arguments("--EMA", "EMA", "Entropy")
    seps = check_cmd_arguments("--seps", "NoParams", False)
    if subplot == "NoHW":
        print("--subplot: No height and width passed.")
        print("--subplot: Pass height and width like; --subplot \"H:W\" ")
        exit(1)

    if seps == "NoParams":
        print("--seps: No lengths passed")
        print("--seps: Pass the length of each sequence to seperate")
        print("--seps: Example \"Length1:Length2:...:step_size\"")
        exit(1)


    if subplot != False:
        subplot = subplot.split(":")
        h = int(subplot[0])
        w = int(subplot[1])
        sub_plotter(files, save, title, xlabel, ylabel, key_to_plot, hide, h, w)
    elif seps != False:
        seps_plotter_single_file(files[0], save, title, xlabel, ylabel, key_to_plot, hide, seps.split(":"))
    else:
        plotter(files, save, title, xlabel, ylabel, key_to_plot, sep_lr, hide)
