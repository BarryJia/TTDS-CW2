
# how to use:
# python check_classification_format.py <your_submission_file_here>

import sys

CORRECT_HEADER = "system,split,p-pos,r-pos,f-pos,p-neg,r-neg,f-neg,p-neu,r-neu,f-neu,p-macro,r-macro,f-macro"

def check_file(path, verbose=True):
    correct = True
    seen_system_split_combos = set([])
    with open(path) as infile:
        header = infile.readline().strip()
        if header != CORRECT_HEADER:
            if verbose:
                print("Header is missing or incorrect, it should be (exactly):")
                print(CORRECT_HEADER)
            correct = False
        for i,line in enumerate(infile.readlines()):
            line = line.strip()
            parts = line.split(',')
            if len(parts) != 14:
                if verbose:
                    print(f"Incorrect number of columns in line {i+1}. Expected:14, Got:{len(parts)}")
                correct = False
            else:
                system,split,p_pos,r_pos,f_pos,p_neg,r_neg,f_neg,p_neu,r_neu,f_neu,pm,rm,fm = line.split(',')
                if (system,split) in seen_system_split_combos:
                    if verbose:
                        print(f"duplicate (system,split) pair on line {i+1}:{(system,split)}")
                    correct = False
                seen_system_split_combos.add( (system,split) )
                if system not in 'baseline improved'.split():
                    if verbose:
                        print(f"Invalid system name: {system}")
                    correct = False
                if split not in 'train dev test'.split():
                    if verbose:
                        print(f"Invalid split: {split}")
                    correct = False
                for j,score in enumerate([p_pos,r_pos,f_pos,p_neg,r_neg,f_neg,p_neu,r_neu,f_neu,pm,rm,fm]):
                    try:
                        float_score = float(score)
                    except:
                        if verbose:
                            print(f"Invalid score on line {i+1}, col {j+1}: {score}")
                        correct = False
        for system in 'baseline improved'.split():
            for split in 'train dev test'.split():
                if (system,split) not in seen_system_split_combos:
                    if verbose:
                        print("Missing (system,split) pair:",(system,split))
                    correct = False
        if correct and verbose:
            print("File is in correct format.")
    return correct

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python check_classification_format.py <your_submission_file>")
    else:
        check_file(sys.argv[1])
