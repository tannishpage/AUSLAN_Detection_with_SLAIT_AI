import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
from detector import check_cmd_arguments

def get_files():
    for i, arg in enumerate(sys.argv[1:]):
        if "--" in arg:
            return sys.argv[1:i+1]
            

def plotter(files, save, title, xlabel, ylabel, sep_lr):
    """    fig = plt.figure(1)
    fig.set_size_inches((19.2, 10.8))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    if plot_loc != "":
        fig.savefig(plot_loc, dpi=100)
    plt.show()"""
    pass

if __name__ == "__main__":

    USAGE = """Usage: python3 plotter.py <path_to_entropy_csv> [<path_to_entropy_csv>..] [options]

        --help          Display this help message
        --save          Saves plot to specified location
        --title         Title of the graph
        --xlabel        Label for x-Axis
        --ylabel        Label for y-Axis
        --sep_lr        Plot left and right hands seperately (Only if --average was used with detector)
"""

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
    
    if not os.path.exists(os.path.base(save)):
        print("--save: Path does not exist")
        exit(1)

    title = check_cmd_arguments("--title", "", "")
    xlabel = check_cmd_arguments("--xlabel", "", "")
    ylabel = check_cmd_arguments("--ylabel", "", "")
    sep_lr = check_cmd_arguments("--sep_lr", True, False)

    plotter(files, save, title, xlabel, ylabel, sep_lr)
