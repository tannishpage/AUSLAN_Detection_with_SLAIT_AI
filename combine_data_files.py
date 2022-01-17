import sys
import os
from detector import get_symbols
import random

def combine(data_files, output_dir):
    all_labels = []
    all_left_hand = []
    all_right_hand = []
    all_frame_number = []
    for file in data_files:
        print("Adding: ", file)
        label = get_symbols("label", file)
        left_hand = get_symbols("left", file)
        right_hand = get_symbols("right", file)
        frame_number = get_symbols("frame", file)
        print(f"File has {frame_number[-1]} frames")
        all_labels += label
        all_left_hand += left_hand
        all_right_hand += right_hand
        all_frame_number += frame_number

    data_file = open(output_dir, 'w')
    data_file.write(f"frame:{','.join(all_frame_number)}\n\
left:{','.join(all_left_hand)}\n\
right:{','.join(all_right_hand)}\nlabel:{','.join(all_labels)}")
    print("Finished Combining")

def main():
    USAGE = """Usage: python3 combine_data_files.py <path_to_data_files> -o <output dir> [options]
   OR: python3 combine_data_files.py data_file_1 data_file_2 [data_file_3...] -o <output dir> [options]

        -o                  The output directory for the combined file
        --randomize         Will combine the files in a random order
        --seed              A seed to use to initialize random
            """
    if len(sys.argv) < 3:
        print(USAGE)
        exit(1)

    randomize = "--randomize" in sys.argv
    seed_flag = "--seed" in sys.argv
    # If no seed is provided, then no seed is initialized
    if seed_flag:
        # Use seed provided by user.
        random.seed(sys.argv[sys.argv.index("--seed")+1])

    output_dir = sys.argv[sys.argv.index("-o")+1]

    if os.path.isdir(sys.argv[1]):
        # First version of comand is passed
        data_files = [os.path.join(sys.argv[1], x) for x in os.listdir(sys.argv[1])
                        if x.endswith(".txt")]

    elif os.path.isfile(sys.argv[1]):
        # Second version of command is passed
        # Since -o is compulsary, and must come after all the files
        # we can use it's index to indicate the end of out file list
        data_files = sys.argv[1:sys.argv.index("-o")]

    else:
        # Something is wrong with the command
        print(USAGE)
        exit(1)

    if randomize:
        # Only shuffle if user wants to randomize
        random.shuffle(data_files)

    combine(data_files, output_dir) # Run combine function on data files




if __name__ == "__main__":
    main()
