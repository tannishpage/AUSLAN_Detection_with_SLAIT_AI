"""
TODO :
- Try to combine left and right hand symbols to form a symbol set of size 64

AA, AB, AC, AD, AE, AF, AG, AH
BA, BB, BC, BD, BE, BF, BG, BH
CA, CB, CC, CD, CE, CF, CG, CH
DA, DB, DC, DD, DE, DF, DG, DH
EA, EB, EC, ED, EE, EF, EG, EH
FA, FB, FC, FD, FE, FF, FG, FH
GA, GB, GC, GD, GE, GF, GG, GH
HA, HB, HC, HD, HE, HF, HG, HH
"""

from slaitai_entropy import FastEntropyNgram, FastEntropy4, ShannonEntropy, String2NGramList
import random
import matplotlib.pyplot as plt
import sys

def generate_random_seq(n, alphabets):
    """
    Generates a random string of text containing only alphabets

    Parameters
        - alphabets (string or list): The alphabet to use to generate the string
        - n (int): The size of the string to generate

    Returns
        A randomly generated string
    """
    random.seed(420) # For repetability of experiment
    #sentence = "thequickbrownfoxjumpedoverthelazydog"
    string = [random.choice(alphabets) for x in range(0, n)]
    random_numbers = set()

    #This code is redundent but fun to play with
    #for i in range(0, 1):
    #    x = random.randint(0, len(string))
    #    while x in random_numbers:
    #        x = random.randint(0, len(string))
    #    for j, e in enumerate(range(x, x+len(sentence))):
    #        string[e] = sentence[j]
    #        random_numbers.add(j)

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
    freq_dist.sort(key=lambda x: x[1], reverse=True) # Sort based on second value, in descending order
    return freq_dist

def calculate_entropy(string, sample_size, ap, bp, cp):
    N = len(string)
    entropies = []
    start = 0
    for i, end in enumerate(range(sample_size, N, sample_size)):
        sub_string = string[start:end+1]
        freq_dist = sorted_freq_dist(sub_string)
        most_freq = freq_dist[0][0] # Most frequent symbol
        entropies.append(FastEntropy4(sub_string, len(sub_string), most_freq, len(freq_dist), ap, bp, cp)[0])
        print(i+1, string[start:end+1])
        start = end

    return (range(sample_size, N, sample_size), entropies)

def convert_left_right_to_one_string(left_string, right_string):
    new_string = []
    for left, right in zip(left_string, right_string):
        new_string.append(left+right)

    return new_string
def main():
    # Running with random characters and graphing
    string = generate_random_seq(5000, 'abcdefghijklmnopqrstuvwxyz') # We have a unigram
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    x, y = calculate_entropy(string, 50, ap, bp, cp)
    plt.plot(x, y)
    plt.title("Graph Of Entropy")
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.show()

def compare_entropies(string1, string2, sample_size):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    string = strip_everything_but_characters(string1)
    x1, y1 = calculate_entropy(string, sample_size, ap, bp, cp)
    plt.plot(x1, y1, color='blue')
    string = strip_everything_but_characters(string2)
    x2, y2 = calculate_entropy(string, sample_size, ap, bp, cp)
    plt.plot(x2, y2, color='orange')
    plt.title("Graph Of Entropy")
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.legend(["String 1", "String 2"])
    plt.show()


def singular_string(string, sample_size):
    ap = 0.0095
    bp = 4.0976
    cp = 3.9841
    #string = strip_everything_but_characters(string)
    x, y = calculate_entropy(string, sample_size, ap, bp, cp)
    plt.plot(x, y, color='blue')
    plt.title("Graph Of Entropy")
    plt.xlabel("String Location")
    plt.ylabel("Fast Entropy Value")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test.py <path_to_text_file> [<path_to_text_file> --combine]")
        exit(0)
    if len(sys.argv) > 4:
        print("Usage: python3 test.py <path_to_text_file> [<path_to_text_file> --combine]")
        exit(0)
    if len(sys.argv) == 2:
        string = open(sys.argv[1], 'r').read()
        string = strip_everything_but_characters(string)
        freq_dist = sorted_freq_dist(string)
        prob_dist = {}
        for t in freq_dist:
            prob_dist[t[0]] = t[1]
        singular_string(string, 30)
    elif len(sys.argv) == 3:
        string_one = open(sys.argv[1], 'r').read()
        string_one = strip_everything_but_characters(string_one)
        freq_dist_one = sorted_freq_dist(string_one)
        prob_dist_one = {}
        for t in freq_dist_one:
            prob_dist_one[t[0]] = t[1]

        string_two = open(sys.argv[2], 'r').read()
        string_two = strip_everything_but_characters(string_two)
        freq_dist_two = sorted_freq_dist(string_two)
        prob_dist_two = {}
        for t in freq_dist_two:
            prob_dist_two[t[0]] = t[1]
        compare_entropies(string_one, string_two, 30)
    else:
        string_one = open(sys.argv[1], 'r').read()
        string_one = strip_everything_but_characters(string_one)
        string_two = open(sys.argv[2], 'r').read()
        string_two = strip_everything_but_characters(string_two)
        string = convert_left_right_to_one_string(string_one, string_two)
        freq_dis = sorted_freq_dist(string)
        singular_string(string, 30)
