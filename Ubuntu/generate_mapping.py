import random
import os

symbols = ['grave', 'minus', 'equal', 'asciitilde', 'exclam', 'at', 'numbersign', 'dollar', 'percent', 'asciicircum', 'ampersand', 'asterisk', 'parenleft', 'parenright', 'underscore', 'plus', 'bracketleft', 'bracketright', 'braceleft', 'braceright', 'semicolon', 'colon', 'apostrophe', 'quotedbl', 'comma', 'less', 'greater', 'period', 'slash', 'question', 'backslash', 'bar']

chars = [chr(ord('a') + i) for i in range(26)]
upper = [chr(ord('A') + i) for i in range(26)]
chars.extend(upper)
nums = [chr(ord('0') + i) for i in range(10)]

all_symbols = []
all_symbols.extend(symbols)
all_symbols.extend(chars)
all_symbols.extend(nums)

header = 'default  partial alphanumeric_keys modifier_keys\nxkb_symbols \"basic\" {\n\n    name[Group1]= "English (Custom)";\n\n'

tail = '};'

keys = ['TLDE']
limits = [12, 12, 11, 10]
letters = ['AE', 'AD', 'AC', 'AB']

for i in range(4):
    for j in range(1, 12):
        if j < 10:
            keys.append(letters[i] + '0' + str(j))
        else:
            keys.append(letters[i] + str(j))
keys.append('BKSL')

body = ""
for key in keys:
    index_one = random.randint(0, len(all_symbols) - 1)
    index_two = random.randint(0, len(all_symbols) - 1)
    body += "    key <" + key + "> {  [ " + all_symbols[index_one] + ", " + all_symbols[index_two] + " ] };\n"

symbol_file = '/usr/share/X11/xkb/symbols/cu'
with open(symbol_file, 'w') as f:
    f.write(header + body + tail)









