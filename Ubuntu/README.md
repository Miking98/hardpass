# HardPass Windows System

## Prerequisites

Ubuntu 18.04 machine, with an installation of Python 2.7 or Python 3. 

## Installation

Note: installation requires Administrator privileges.

First, generate the HardPass mapping file:
```
sudo python3 generate_mapping.py
```

Then, set up keyboard shortcuts for the following two commands. We suggest using ```Ctrl + Left Arrow``` and ```Ctrl + Right Arrow```,
as these keys will not be remapped by HardPass.

```
setxkbmap us
setxkbmap cu
```

The former command will change the keyboard layout to the standard English (US) layout,  whereas the latter will change the layout to the custom HardPass layout.

Finally, restart your computer. You can access the HardPass layout using your shortcut!

