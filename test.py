import os
import sys

keys_to_hash = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']

def hash_key(key):
    """
    Hashes the key into 3-4 "random" keys
    """
    rtn = ""
    hashed_str = 'abcd'
    for s in hashed_str:
        rtn += "00" + s.encode("hex") + "  "
    return rtn

if __name__ == "__main__":
    print('Hello, world!')
    
    fw = open("tmp.klc", "w")

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
