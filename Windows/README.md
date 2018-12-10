# HardPass Windows System

## Prerequisites

Windows 10 machine, with an installation of Python 2.7 or Python 3. 

## Installation

Note: installation requires Administrator privileges, so it is necessary to open the Command Prompt as Administrator (`ctrl + shift + enter` on most machines). 

First, generate the HardPass `.klc` file:
```
python generate_keyboard.py
```

Then, install the HardPass keyboard:
```
python install_keyboard.py hardpass.klc
```

Finally, restart your computer.  Your HardPass keyboard will now appear in the dropdown list of keyboards!

## Troubleshooting

If the above process doesn't work for any reason, try downloading Microsoft Keyboard Layout Creator 1.4 (https://www.microsoft.com/en-us/download/details.aspx?id=22339), and then follow the steps above.
