from slaitai_entropy import FastEntropyNgram, FastEntropy4, ShannonEntropy, String2NGramList
import random
import matplotlib.pyplot as plt
import sys
import os
random.seed(128) # Helps repetability of experiments

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
        - prob_dist (dict{symbol:probability}): Probability distribution to follow
    """

    return random.choices(list(prob_dist.keys()), weights=list(prob_dist.values()), k=n)


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

def calculate_entropy(string, sample_size, ap, bp, cp):
    N = len(string)
    entropies = []
    start = 0
    for i, end in enumerate(range(sample_size, N, sample_size)):
        sub_string = string[start:end+1]
        freq_dist = sorted_freq_dist(sub_string)
        most_freq = freq_dist[0][0] # Most frequent symbol
        entropies.append(FastEntropy4(sub_string, len(sub_string), most_freq,
                                        len(freq_dist), ap, bp, cp)[0])
        print(i+1, string[start:end+1])
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
        if line.startswith(key):
            values = line.split(":")[1].split(",")
            return values
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
    for file in files:
        left = get_symbols("left", file)
        right = get_symbols("right", file)
        symbols_left.append(left)
        symbols_right.append(right)
    return symbols_left, symbols_right
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
                        legend=["String 1", "String 2"],
                        title="Graph of Entropy"):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    for string in strings:
        x, y = calculate_entropy(string, sample_size, ap, bp, cp)
        plt.plot(x, y)

    plt.title(title)
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.legend(legend)
    plt.show()

def perform_experiement(files, combine):
    left_symbols, right_symbols = get_values_from_file(files)
    if combine:
        combined_strings = []
        for left, right in zip(left_symbols, right_symbols):
            combined_strings.append(combine_left_right(left, right))
        compare_entropies(combined_strings, 64, files)
    else:
        compare_entropies(left_symbols+right_symbols, 16, [x+"_LEFT" for x in files] + [x+"_RIGHT" for x in files])

if __name__ == "__main__":
    USAGE = """Usage: python3 detector.py <path_to_text_file> [<path_to_text_file>] [options]
   OR: python3 detector.py <path_to_text_files> [options]

        --combine           Will combine the left and right hand to make a symbol set of size 64
        --sample_size       The number of samples to use to calculate entropy. Default is 64 for combine and 16 for normal
            """
    if len(sys.argv) < 2:
        print(USAGE)
        exit(0)
    if len(sys.argv) > 4:
        print(USAGE)
        exit(0)
    combine = "--combine" in sys.argv

    # Check if the first path is a file or a folder
    if os.path.isfile(sys.argv[1]):
        if len(sys.argv) >= 3 and os.path.isfile(sys.argv[2]): # Check if we have another file
            perform_experiement(sys.argv[1:3], combine)
        else:# Else we can proceed with one file
            perform_experiement(sys.argv[1:2], combine)

    else:
        # We have a folder, so we handel it like a folder
        perform_experiement([os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if os.path.join(sys.argv[1], f) and f.endswith(".txt")], combine)
