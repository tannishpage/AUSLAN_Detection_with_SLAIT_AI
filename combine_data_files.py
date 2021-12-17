import sys
import os
from detector import get_values_from_file
import random

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 combine_data_files.py <path_to_data_files> <output dir>")
        exit(1)

    data_files = [os.path.join(sys.argv[1], x) for x in os.listdir(sys.argv[1])
                    if x.endswith(".txt")]

    left_symbols, right_symbols = get_values_from_file(data_files)
    left = []
    right = []
    count = 0
    for l, r in zip(left_symbols, right_symbols):
        print(data_files[count])
        left +=  l
        right += r
        count += 1
    file = open(os.path.join(sys.argv[2], "data.txt"), 'w')
    file.write(f"left:{','.join(left)}\nright:{','.join(right)}")
    file.close()

if __name__ == "__main__":
    main()
