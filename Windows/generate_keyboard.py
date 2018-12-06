import os
import sys
import random

keys_to_hash = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']
specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

def hash_key(key):
    """
    Hashes the key into 3-4 "random" keys
    """

    # p(3 chars) = 0.25, p(4 chars) = 0.75
    length = 3
    if random.random() >= 0.25:
        length = 4

    rtn = ""
    for _ in range(length):
        kind = random.randint(0, 2)
        if kind == 0:
            c = random.choice(numbers)
        elif kind == 1:
            c = random.choice(letters)
        else:
            c = random.choice(specials)
        rtn += "00" + c.encode("hex") + "  "

    return rtn

if __name__ == "__main__":
    """ Script that generates a new randomized keyboard file, hardpass.klc"""

    fw = open("hardpass.klc", "w")

    # Write beginning
    lines_to_write = []
    with open("ground_truth.txt", "r") as ground:
        for line in ground:
            lines_to_write.append(line)
            if line.find("LIGATURE") >= 0:
                break
    lines_to_write.append('\n')
    fw.writelines(lines_to_write)

    # Write hashed keys
    # Format: VK_   Mod#    Char0   Char1   Char2   Char3
    lines_to_write = []
    for key in keys_to_hash:
        for mod in range(2):
            line = "{}  {}  ".format(key, mod)
            line += hash_key(key) + "\n"
            lines_to_write.append(line)
    lines_to_write.append('\n')
    fw.writelines(lines_to_write)

    # Write end
    lines_to_write = []
    with open("ground_truth.txt", "r") as ground:
        write = False
        for line in ground:
            if line.find("KEYNAME") >= 0:
                write = True
            if write:
                lines_to_write.append(line)
    fw.writelines(lines_to_write)
    fw.close()
