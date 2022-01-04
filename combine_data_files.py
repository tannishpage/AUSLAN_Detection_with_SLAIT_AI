import sys
import os
from detector import get_symbols
import random

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 combine_data_files.py <path_to_data_files> <output dir>")
        exit(1)

    data_files = [os.path.join(sys.argv[1], x) for x in os.listdir(sys.argv[1])
                    if x.endswith(".txt")]
    output_dir = sys.argv[2]
    all_labels = []
    all_left_hand = []
    all_right_hand = []
    all_frame_number = []
    for file in data_files:
        label = get_symbols("label", file)
        left_hand = get_symbols("left", file)
        right_hand = get_symbols("right", file)
        frame_number = get_symbols("frame", file)
        all_labels += label
        all_left_hand += left_hand
        all_right_hand += right_hand
        all_frame_number += frame_number

    data_file = open(os.path.join(sys.argv[2], "data.txt"), 'w')
    data_file.write(f"frame:{','.join(all_frame_number)}\nleft:{','.join(all_left_hand)}\nright:{','.join(all_right_hand)}\nlabel:{','.join(all_labels)}")

if __name__ == "__main__":
    main()
