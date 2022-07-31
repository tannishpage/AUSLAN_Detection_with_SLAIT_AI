from slaitai_entropy import FastEntropyNgram, FastEntropy4, ShannonEntropy, String2NGramList, FastEntropyNgram
import random
import matplotlib.pyplot as plt
import sys
import os
import math
import numpy
import pandas as pd
random.seed(128) # Helps repetability of experiments

def check_cmd_arguments(arg, default, false_value):
    arg_value = false_value # Setting the argument's value to the false value
    # Checking if argument is in the sys args
    if arg in sys.argv:
        index = sys.argv.index(arg) + 1 # Grab the index of the value for arg
        if index >= len(sys.argv):
        # If the value isn't passed, set it to the default value
            arg_value = default
        else:
            # We check that the value isn't another argument
            value = sys.argv[index]
            if "-" not in value:
                arg_value = value # Assign the value
            else:
                arg_value = default # else we use use the default value

    return arg_value

def get_files():
    for i, arg in enumerate(sys.argv[1:]):
        if "--" in arg:
            return sys.argv[1:i+1]
    return sys.argv[1:]

def generate_random_seq(n, alphabets):
    """
    Generates a random string of text containing only alphabets

    Parameters
        - alphabets (string or list): The alphabet to use to generate the string
        - n (int): The size of the string to generate

    Returns
        A randomly generated string
    """
    string = [random.choice(alphabets) for x in range(0, n)]
    random_numbers = set()
    return string

def generate_random_seq_with_probs(n, prob_dist):
    """
    Generates a random string of text that follows the probability distribution
    given

    Parameters
        - n (int): The size of the string to generate
        - prob_dist (dict{symbol:probability}): Probability distribution to
                                                follow
    """

    return random.choices(list(prob_dist.keys()),
                                weights=list(prob_dist.values()), k=n)


def strip_everything_but_characters(text):
    """
    Given some text will remove everything except for alphabets and will
    convert everything to lower case

    Parameters
        - text (string): The text from which we want to remove everything but
                            alphabets
    Returns
        A string
    """
    stripped_text = ''

    for c in text:
        if (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122):
            stripped_text += c.lower()
    return stripped_text

def get_alphabets(symbols):
    alphabets = set()
    for symbol in symbols:
        if type(symbol) == type(list()):
            symbol = tuple(symbol)
        alphabets.add(symbol)
    return list(alphabets)

def sorted_freq_dist(symbols):
    alphabets = get_alphabets(symbols)
    freq_dist = []

    for alphabet in alphabets:
        freq_dist.append((alphabet, symbols.count(alphabet)))
    # Sort based on second value, in descending order
    freq_dist.sort(key=lambda x: x[1], reverse=True)
    return freq_dist

def calculate_entropy(string, sample_size, ap, bp, cp, hand="combine"):
    N = len(string)
    entropies = []
    start = 0
    count = 0
    probs = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}
    if sample_size == -1:
        sample_size = len(string) - 1
    for i, end in enumerate(range(sample_size, N, sample_size)):
        sub_string = string[start:end+1]
        freq_dist = sorted_freq_dist(sub_string)

        # Using Rank 1 for every sample, the rank changes for each sample
        most_freq = freq_dist[0][0] # Most frequent symbol
        entropy, prob_dist = FastEntropy4(sub_string, len(sub_string), most_freq,
                                        len(freq_dist), ap, bp, cp)
        entropies.append(entropy)

        for i, freq in enumerate(freq_dist):
            if probs.get(freq[0], None) == None:
                probs[freq[0]] = [prob_dist[i]]
            else:
                probs[freq[0]].append(prob_dist[i])
        count += 1
        for s in probs.keys():
            if len(probs[s]) < count:
                probs[s].append(0.0)

        #print(i+1, string[start:end+1])
        start = end

    #print(probs)
    fig = plt.figure()
    fig.set_size_inches((19.2, 10.8))
    plt.title(hand)
    for i, symbol in enumerate(probs.keys()):
        plt.subplot(3, 3, i+1)
        plt.plot(range(0, len(probs[symbol])), probs[symbol])
        plt.ylim(0, 1)
        plt.xlabel("Frame")
        plt.ylabel("Probability")
        plt.legend(symbol)
    #plt.show()
    fig.savefig(f"./{hand}_plot.png", dpi=100)

    return (range(sample_size, N, sample_size), entropies)

def calculate_ngram_entropy(string, sample_size, ap, bp, cp):
    N = len(string)
    entropies = []
    start = 0
    for i, end in enumerate(range(sample_size, N, sample_size)):
        sub_string = string[start:end+1]
        freq_dist = sorted_freq_dist(sub_string)
        most_freq = freq_dist[0][0]
        if type(most_freq) == type(tuple()):
            most_freq = list(most_freq)
        entropies.append(FastEntropyNgram(sub_string, len(sub_string),
                                          most_freq,
                                          len(freq_dist), ap, bp, cp)[0])
        #print(i+1, string[start:end+1])
        start = end
    return (range(sample_size, N, sample_size), entropies)

def combine_left_right(left_string, right_string):
    new_string = []
    for left, right in zip(left_string, right_string):
        new_string.append(left+right)

    return new_string

def get_symbols(key, file_name):
    """
    Retrieves the values from a file formatted in the following way

    key:value1,value2,value3,... etc

    Parameters
        - key (string): The key to look for
        - file_name (string): the name of the file to look for the key in
    Returns
        A list of values
    """
    file = open(file_name, 'r')
    for line in file.readlines():
        line = line.rstrip()
        if line.startswith(key) or (key in line.split(":")[0]):
            values = line.split(":")[1].split(",")
            return values

def get_values_from_csv(files):
    symbols_left = []
    symbols_right = []
    labels = []

    for file in files:
        data = pd.read_csv(file)

        left = list(data["Left"])
        right = list(data["Right"])
        symbols_left.append(left)
        symbols_right.append(right)

    return symbols_left, symbols_right


def get_values_from_file(files):
    """
    Takes a list of files and returns a tuple of the left and right symbols
    within each file as a list of lists per file

    Parameters
        - files (list<string>) : a list of file names of strings
    Returns
        A tuple<list<list<string>> where each list within the second level will
        be organized according to the files list
    """
    symbols_left = []
    symbols_right = []
    labels = []
    for file in files:
        left = get_symbols("left", file)
        right = get_symbols("right", file)
        label = get_symbols("label", file)
        label = [int(l) for l in label]
        symbols_left.append(left)
        symbols_right.append(right)
        labels.append(label)
    return symbols_left, symbols_right, labels

def calculate_average(left, right):
    average = []
    for l, r in zip(left, right):
        average.append((l+r)/2)
    return average

def create_segments(labels, sample_size):
    start = 0
    seg_labels = []
    for end in range(sample_size, len(labels), sample_size):
        if sum(labels[start:end])/sample_size >= 0.5:
            seg_labels.append(1)
        else:
            seg_labels.append(0)
        start = end
    return seg_labels

def simple_moving_average(values, sample_size):
    # Calculate first average
    moving_averages = [sum(values[0:sample_size+1])/sample_size]
    removed_index = 0 # The index that was removed from the sample
    for value in values[sample_size+1:]:
        # Calculating simple moving average
        moving_averages.append(moving_averages[-1] +\
                                (value - values[removed_index])/sample_size)
        removed_index += 1 # Increase index so we know the last removed value
    return moving_averages

def exponential_moving_average(values, alpha):
    # First value of moving avg is the first value in the series
    moving_averages = [values[0]]
    for value in values[1:]:
        # Calculating simple moving average
        moving_averages.append(moving_averages[-1] +\
                                (alpha*(value - moving_averages[-1])))
    return moving_averages

############### Functions to run experiments ###############
def main():
    # Running with random characters and graphing
    # We have a unigram
    string = generate_random_seq(5000, 'abcdefghijklmnopqrstuvwxyz')
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    x, y = calculate_entropy(string, 50, ap, bp, cp)
    plt.plot(x, y)
    plt.title("Graph Of Entropy")
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.show()

def compare_entropies(strings, sample_size,
                      labels, moving_averages, data_loc):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    data = dict()
    #print(len(strings))
    if labels != None:
        seg_labels = create_segments(labels[0], sample_size)
    for i, string in enumerate(strings):
        x, y = calculate_entropy(string, sample_size, ap, bp, cp)
        data["Frame Number"] = x
        data["Entropy"] = y
        if labels != None:
            data["Label"] = seg_labels
    if moving_averages != 0:
        entropies = [entropy if str(entropy) != 'nan' else 0.0 for entropy in y]
        averages = exponential_moving_average(entropies, moving_averages)
        data["EMA"] = averages

    data_frame = pd.DataFrame(data)
    data_frame.to_csv(data_loc)


def compare_entropies_average(left, right, sample_size,
                              labels, moving_averages, data_loc, file_name):

    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    data = dict()
    if labels != None:
        seg_labels = create_segments(labels[0], sample_size)
    for l, r in zip(left, right):
        maximum = min(len(l), len(r))
        x, y_l = calculate_entropy(l[:maximum], sample_size, ap, bp, cp, f"{file_name} Left Hand")
        x, y_r = calculate_entropy(r[:maximum], sample_size, ap, bp, cp, f"{file_name} Right Hand")
        y_avg = calculate_average(y_l, y_r)
        print(len(x), len(y_l), len(y_r), len(y_avg))
        data["Frame Number"] = x
        data["Left Entropy"] = y_l
        data["Right Entropy"] = y_r
        data["Entropy"] = y_avg
        if labels != None:
            data["Label"] = seg_labels
    if moving_averages != 0:
        entropies = [entropy if str(entropy) != 'nan' else 0.0 for entropy in y_avg]
        averages = exponential_moving_average(entropies, moving_averages)
        print(len(averages))
        data["EMA"] = averages

    data_frame = pd.DataFrame(data)
    data_frame.to_csv(data_loc)

def compare_entropies_ngram_average(left, right, sample_size,
                                    labels, moving_averages, data_loc):

    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    data = dict()
    if labels != None:
        seg_labels = create_segments(labels, sample_size)

    x, y_l = calculate_ngram_entropy(left, sample_size, ap, bp, cp)
    x, y_r = calculate_ngram_entropy(right, sample_size, ap, bp, cp)

    y_avg = calculate_average(y_l, y_r)
    data["Frame Number"] = x
    data["Left Entropy"] = y_l
    data["Right Entropy"] = y_r
    data["Entropy"] = y_avg
    if labels != None:
        data["Label"] = seg_labels
    if moving_averages != 0:
        entropies = [entropy if str(entropy) != 'nan' else 0.0 for entropy in y_avg]
        averages = exponential_moving_average(entropies, moving_averages)
        data["EMA"] = averages

    data_frame = pd.DataFrame(data)
    data_frame.to_csv(data_loc)
def compare_entropies_ngram(strings, sample_size,
                            labels, moving_averages, data_loc):

    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    data = dict()
    if labels != None:
        seg_labels = create_segments(labels, sample_size)

    x, y = calculate_ngram_entropy(strings, sample_size, ap, bp, cp)
    data["Frame Number"] = x
    data["Entropy"] = y
    if labels != None:
        data["Label"] = seg_labels

    if moving_averages != 0:
        entropies = [entropy if str(entropy) != 'nan' else 0.0 for entropy in y]
        averages = exponential_moving_average(entropies, moving_averages)
        data["EMA"] = averages

    data_frame = pd.DataFrame(data)
    data_frame.to_csv(data_loc)

def perform_ngram_experiment(files, combine, average, sample_size, ngram,
                             plot_labels, moving_averages, data_loc):

    if (files[0].endswith(".csv")):
        left_symbols, right_symbols = get_values_from_csv(files)
        data_loc = data_loc.format(files[0].replace(".csv", "_Entropy"))
    else:
        left_symbols, right_symbols, labels = get_values_from_file(files)
        data_loc = data_loc.format(files[0].replace(".txt", "_Entropy"))
    left_symbols = "".join(left_symbols[0])
    right_symbols = "".join(right_symbols[0])

    if not plot_labels:
        labels = None
    else:
        labels = labels[0]

    if average:
        left_ngram = String2NGramList(left_symbols, ngram)[0]
        right_ngram = String2NGramList(right_symbols, ngram)[0]

        compare_entropies_ngram_average(left_ngram, right_ngram, sample_size,
                                        labels, moving_averages, data_loc)
    elif combine:
        combined_string = combine_left_right(left_symbols, right_symbols)
        combined_ngram = String2NGramList(combined_string, ngram)[0]
        compare_entropies_ngram(combined_ngram, sample_size,
                                labels, moving_averages, data_loc)

    else:
        print("Please use --average or --combine when using ngram > 1")
        exit(1)


def perform_experiement(files, combine, average, sample_size,
                        plot_labels, moving_averages, data_loc):

    if (files[0].endswith(".csv")):
        left_symbols, right_symbols = get_values_from_csv(files)
        data_loc = data_loc.format(files[0].replace(".csv", "_Entropy"))
    else:
        left_symbols, right_symbols, labels = get_values_from_file(files)
        data_loc = data_loc.format(files[0].replace(".txt", "_Entropy"))
    if not plot_labels:
        labels = None
    if combine:
        combined_strings = []
        for left, right in zip(left_symbols, right_symbols):
            combined_strings.append(combine_left_right(left, right))
        compare_entropies(combined_strings, sample_size,
                          labels, moving_averages, data_loc)
    else:
        if average:
            print(len(left_symbols) - len(right_symbols))
            compare_entropies_average(left_symbols, right_symbols, sample_size,
                                      labels, moving_averages, data_loc, os.path.basename(files[0]).replace(".txt", ""))
        else:
            compare_entropies(left_symbols+right_symbols, sample_size,
                              labels, moving_averages, data_loc)

if __name__ == "__main__":
    USAGE = """Usage: python3 detector.py <path_to_text_file> [<path_to_text_file>] [options]

        -h, --help          Display this help message
        -s                  Saves data to specified location as a csv file
        --combine           Will combine the left and right hand to make a symbol set of size 64
        --sample_size       The number of samples to use to calculate entropy. Default is 64 for combine and 16 for normal
        --average           Averages the left and right entropies, Not applicable with --combine
        --ngram             The n-gram to use for entropy calculation, default is 1 (unigrams)
        --plot_labels       Will plot labels in the entropy graph can't use with csv files
        --moving_averages   Compute and plot moving averages of entropy on top of the entropy. Default sample size is 25
"""
    if len(sys.argv) < 2:
        print(USAGE)
        exit(1)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(USAGE)
        exit(0)

    combine = "--combine" in sys.argv
    average = "--average" in sys.argv
    plot_labels = "--plot_labels" in sys.argv

    moving_averages = float(check_cmd_arguments("--moving_averages", 0.15, 0))
    # By default script uses unigrams. If using --ngram, then ngram will be set
    # to user specified number.
    ngram = int(check_cmd_arguments("--ngram", 1, 1))
    data_loc = check_cmd_arguments("-s", "{}.csv", "./data.csv")

    if combine:
        sample_size = int(check_cmd_arguments("--sample_size", -1, 64))
    else:
        sample_size = int(check_cmd_arguments("--sample_size", -1, 16))

    # Check if the first path is a file or a folder
    files = get_files()
    if len(files) >= 1:
        for file in files:
            print(file)
            if ngram > 1:
                perform_ngram_experiment([file], combine, average,
                                         sample_size, ngram,
                                         plot_labels, moving_averages, data_loc)
            else:
                perform_experiement([file], combine, average,
                                    sample_size, plot_labels, moving_averages,
                                    data_loc)
        """else:# Else we can proceed with one file
            if ngram > 1:
                perform_ngram_experiment(files, combine, average,
                                         sample_size, ngram,
                                         plot_labels, moving_averages, data_loc)
            else:
                perform_experiement(files, combine, average,
                                    sample_size, plot_labels, moving_averages,
                                    data_loc)"""

    else:
        print(f"Use --help or -h to see how to use this script")
        exit()
