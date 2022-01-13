from slaitai_entropy import FastEntropyNgram, FastEntropy4, ShannonEntropy, String2NGramList, FastEntropyNgram
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
        freq_dist.append((alphabet, symbols.count(alphabet)/len(symbols)))
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

def calculate_ngram_entropy(string, sample_size, ap, bp, cp):
    N = len(string)
    entropies = []
    start = 0
    for i, end in enumerate(range(sample_size, N, sample_size)):
        sub_string = string[start:end+1]
        freq_dist = sorted_freq_dist(sub_string)
        most_freq = freq_dist[0][0]
        entropies.append(FastEntropyNgram(sub_string, len(sub_string), most_freq,
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
                        title="Graph of Entropy and Labels",
                        labels=None):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    if labels != None:
        seg_labels = create_segments(labels[0], sample_size)
    for i, string in enumerate(strings):
        x, y = calculate_entropy(string, sample_size, ap, bp, cp)
        plt.plot(x, y)
        if labels != None:
            plt.plot(range(sample_size, len(labels[0]), sample_size), seg_labels, 'o')
    plt.title(title)
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.legend(legend+["1 Sign 0 Non-Sign"])
    plt.show()

def compare_entropies_average(left, right, sample_size,
                        legend=["String 1", "String 2"],
                        title="Graph of Entropy and Labels",
                        labels=None):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    if labels != None:
        seg_labels = create_segments(labels[0], sample_size)
    for l, r in zip(left, right):
        x, y_l = calculate_entropy(l, sample_size, ap, bp, cp)
        x, y_r = calculate_entropy(r, sample_size, ap, bp, cp)
        y_avg = calculate_average(y_l, y_r)
        plt.plot(x, y_avg)
        if labels != None:
            plt.plot(range(sample_size, len(labels[0]), sample_size), seg_labels, 'o')
    plt.title(title)
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.legend(legend+["1 Sign 0 Non-Sign"])
    plt.show()

def compare_entropies_ngram_average(left, right, sample_size,
                        legend=["String 1", "String 2"],
                        title="Graph of Entropy and Labels",
                        labels=None):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    if labels != None:
        seg_labels = create_segments(labels, sample_size)

    x, y_l = calculate_ngram_entropy(left, sample_size, ap, bp, cp)
    x, y_r = calculate_ngram_entropy(right, sample_size, ap, bp, cp)

    y_avg = calculate_average(y_l, y_r)
    plt.plot(x, y_avg)
    if labels != None:
        plt.plot(range(sample_size, len(labels), sample_size), seg_labels, 'o')
    plt.title(title)
    plt.xlabel("Ngram Location")
    plt.ylabel("Fast Entropy Value")
    plt.legend(legend+["1 Sign 0 Non-Sign"])
    plt.show()

def perform_ngram_experiment(files, combine, sample_size, ngram, average=False):
    left_symbols, right_symbols, labels = get_values_from_file(files)
    left_symbols = "".join(left_symbols[0])
    right_symbols = "".join(right_symbols[0])
    labels = labels[0]

    if combine:
        print("Can't use combine when ngram > 1")
        exit(1)

    if not average:
        print("Please use average flag when using ngram > 1")
        exit(1)

    left_ngram = String2NGramList(left_symbols, ngram)[0]
    right_ngram = String2NGramList(right_symbols, ngram)[0]

    compare_entropies_ngram_average(left_ngram, right_ngram, sample_size, files,
                            title=f"Graph of {ngram}-gram Entropy and Labels",
                            labels=labels)


def perform_experiement(files, combine, sample_size, average=False):
    left_symbols, right_symbols, labels = get_values_from_file(files)
    if combine:
        combined_strings = []
        for left, right in zip(left_symbols, right_symbols):
            combined_strings.append(combine_left_right(left, right))
        compare_entropies(combined_strings, sample_size, files, labels=labels)
    else:
        if average:
            compare_entropies_average(left_symbols, right_symbols, sample_size, files, labels=labels)
        else:
            compare_entropies(left_symbols+right_symbols, sample_size, [x+"_LEFT" for x in files] + [x+"_RIGHT" for x in files], labels=labels)

if __name__ == "__main__":
    USAGE = """Usage: python3 detector.py <path_to_text_file> [<path_to_text_file>] [options]
   OR: python3 detector.py <path_to_text_files> [options]

        --combine           Will combine the left and right hand to make a symbol set of size 64
        --sample_size       The number of samples to use to calculate entropy. Default is 64 for combine and 16 for normal
        --average           Averages the left and right entropies, Not applicable with --combine
        --ngram             The n-gram to use for entropy calculation, default is 1 (unigrams)
            """
    if len(sys.argv) < 2:
        print(USAGE)
        exit(0)
    if len(sys.argv) > 7:
        print(USAGE)
        exit(0)
    combine = "--combine" in sys.argv
    average = "--average" in sys.argv

    # By default script uses unigrams. If using --ngram, then ngram will be set
    # to user specified number.
    ngram = 1 if "--ngram" not in sys.argv else int(sys.argv[sys.argv.index("--ngram")+1])
    if combine:
        sample_size = 64 if "--sample_size" not in sys.argv else int(sys.argv[sys.argv.index("--sample_size")+1])
    else:
        sample_size = 16 if "--sample_size" not in sys.argv else int(sys.argv[sys.argv.index("--sample_size")+1])

    # Check if the first path is a file or a folder
    if os.path.isfile(sys.argv[1]):
        if len(sys.argv) >= 3 and os.path.isfile(sys.argv[2]): # Check if we have another file
            perform_experiement(sys.argv[1:3], combine, sample_size, average)
        else:# Else we can proceed with one file
            if ngram > 1:
                perform_ngram_experiment(sys.argv[1:2], combine, sample_size, ngram, average)
            else:
                perform_experiement(sys.argv[1:2], combine, sample_size, average)

    else:
        # We have a folder, so we handel it like a folder
        perform_experiement([os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if os.path.join(sys.argv[1], f) and f.endswith(".txt")], combine, sample_size)
