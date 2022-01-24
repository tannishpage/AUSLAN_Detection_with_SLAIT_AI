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


def plotter(files, save, title, xlabel, ylabel, sep_lr, hide):
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
            plt.plot(data["Frame Number"], data["Entropy"])

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

if __name__ == "__main__":

    USAGE = """Usage: python3 plotter.py <path_to_entropy_csv> [<path_to_entropy_csv>..] [options]

        --help          Display this help message
        --save          Saves plot to specified location
        --hide          doesn't show the plot
        --title         Title of the graph
        --xlabel        Label for x-Axis
        --ylabel        Label for y-Axis
        --sep_lr        Plot left and right hands seperately (Only if --average was used with detector)
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

    plotter(files, save, title, xlabel, ylabel, sep_lr, hide)
