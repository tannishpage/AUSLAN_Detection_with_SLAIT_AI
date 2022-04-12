import random
import matplotlib.pyplot as plt
import sys
import os
from detector import get_values_from_file, sorted_freq_dist

def get_sign_non_sign_segments(labels):
    """
    Returns 2 lists with start and end indices
    of sign and non-sign segments
    """
    sign_segs = []
    non_sign_segs = []
    start = 0
    end = -1
    for i, label in enumerate(labels):
        if i == 0:
            continue
        if labels[i-1] != label:
            end = i
            if labels[i-1] == 1:
                sign_segs.append((start, end))
            else:
                non_sign_segs.append((start, end))
            start = i
    return sign_segs, non_sign_segs

def get_all_freq_dists(segs, hand):
    freq_dists = []
    for seg in segs:
        seg_symbols = hand[seg[0]:seg[1]+1]
        freq_dists.append(sorted_freq_dist(seg_symbols))
    return freq_dists

def get_average_dist(dists):
    average_dist = {}
    for dist in dists:
        for symbol in dist:
            if symbol[0] not in average_dist.keys():
                average_dist[symbol[0]] = symbol[1]
            else:
                average_dist[symbol[0]] += symbol[1]
    for symbol in average_dist:
        average_dist[symbol] /= len(dists)
    return average_dist

def analyse_symbols_with_labels(hand, labels):
    """
    Is used to produce a graph of distribution, to show how the symbols are
    distributed during non-sign and sign segments
    """
    sign_segs, non_sign_segs = get_sign_non_sign_segments(labels)
    sign_freq_dist = get_all_freq_dists(sign_segs, hand)
    non_sign_freq_dist = get_all_freq_dists(non_sign_segs, hand)
    average_sign_dist = get_average_dist(sign_freq_dist)
    average_non_sign_dist = get_average_dist(non_sign_freq_dist)
    return average_sign_dist, average_non_sign_dist


if __name__ == "__main__":
    USAGE = """Usage: python3 analyse_symbols.py <path_to_text_file> [options]
        --combine           Will combine the left and right hand to make a symbol set of size 64
            """
    if len(sys.argv) < 2:
        print(USAGE)
        exit(0)
    if len(sys.argv) > 3:
        print(USAGE)
        exit(0)
    combine = "--combine" in sys.argv

    # Check if the first path is a file or a folder
    if os.path.isfile(sys.argv[1]):
        left_symbols, right_symbols, labels = get_values_from_file([sys.argv[1]])
        left_sign, left_non_sign = analyse_symbols_with_labels(left_symbols[0], labels[0])
        right_sign, right_non_sign = analyse_symbols_with_labels(right_symbols[0], labels[0])
        #print(left_sign, left_non_sign)
        #print(right_sign, right_non_sign)
        plt.subplot(2, 2, 1)
        plt.title("Left Signing")
        plt.bar(range(len(left_sign)), list(left_sign.values()), align='center')
        plt.xticks(range(len(left_sign)), list(left_sign.keys()))
        plt.ylabel("Probability")
        plt.subplot(2, 2, 2)
        plt.title("Left Non-Signing")
        plt.bar(range(len(left_non_sign)), list(left_non_sign.values()), align='center')
        plt.xticks(range(len(left_non_sign)), list(left_non_sign.keys()))
        plt.ylabel("Probability")
        plt.subplot(2, 2, 3)
        plt.title("Right Signing")
        plt.bar(range(len(right_sign)), list(right_sign.values()), align='center')
        plt.xticks(range(len(right_sign)), list(right_sign.keys()))
        plt.ylabel("Probability")
        plt.subplot(2, 2, 4)
        plt.title("Right Non-Signing")
        plt.bar(range(len(right_non_sign)), list(right_non_sign.values()), align='center')
        plt.xticks(range(len(right_non_sign)), list(right_non_sign.keys()))
        plt.ylabel("Probability")
        plt.show()
