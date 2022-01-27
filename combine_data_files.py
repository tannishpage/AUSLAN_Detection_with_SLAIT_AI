import sys
import os
from detector import get_symbols
import random

def combine(data_files, output_dir, write):
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
        print(f"File has {len(frame_number)} frames")
        all_labels += label
        all_left_hand += left_hand
        all_right_hand += right_hand
        all_frame_number += frame_number
    if write:
        data_file = open(output_dir, 'w')
        data_file.write(f"frame:{','.join(all_frame_number)}\n\
left:{','.join(all_left_hand)}\n\
right:{','.join(all_right_hand)}\nlabel:{','.join(all_labels)}")
    print("Finished Combining")

    return all_labels, all_left_hand, all_right_hand, all_frame_number

def interleave_data(data, seg_len, output_dir):
    start = 0
    labels = []
    left_hand = []
    right_hand = []
    frame_number = []
    for end in range(seg_len, len(data[0]), seg_len):
        labels.append(data[0][start:end])
        left_hand.append(data[1][start:end])
        right_hand.append(data[2][start:end])
        frame_number.append(data[3][start:end])
        start = end

    random.seed(seg_len)
    random.shuffle(labels)
    random.seed(seg_len)
    random.shuffle(left_hand)
    random.seed(seg_len)
    random.shuffle(right_hand)
    random.seed(seg_len)
    random.shuffle(frame_number)

    all_labels = []
    all_left_hand = []
    all_right_hand = []
    all_frame_number = []

    for index in range(0, len(labels)):
        all_labels += labels[index]
        all_left_hand += left_hand[index]
        all_right_hand += right_hand[index]
        all_frame_number += frame_number[index]

    print("Done")
    print("Writing to file...")
    data_file = open(output_dir, 'w')
    data_file.write(f"frame:{','.join(all_frame_number)}\n\
left:{','.join(all_left_hand)}\n\
right:{','.join(all_right_hand)}\nlabel:{','.join(all_labels)}")
    print("Done")

def main():
    USAGE = """Usage: python3 combine_data_files.py <path_to_data_files> -o <output dir> [options]
   OR: python3 combine_data_files.py data_file_1 data_file_2 [data_file_3...] -o <output dir> [options]

        -o                  The output directory for the combined file
        --randomize         Will combine the files in a random order
        --seed              A seed to use to initialize random
        --interleave        Will take segments and insert them in random spots
        --seg_len           The length of segment to interleave
            """
    if len(sys.argv) < 3:
        print(USAGE)
        exit(1)

    print(sys.argv)
    randomize = "--randomize" in sys.argv
    seed_flag = "--seed" in sys.argv
    interleave = "--interleave" in sys.argv
    seg_len = 1500 if "--seg_len" not in sys.argv else int(sys.argv[sys.argv.index("--seg_len")+1])
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

    # Will combine data files and write to file
    all_data = combine(data_files, output_dir, not interleave)

    if interleave:
        # If we need to interlave, we will take the combined
        # and interleave
        print("Interleaving data...")
        interleave_data(all_data, seg_len, output_dir)


if __name__ == "__main__":
    main()
