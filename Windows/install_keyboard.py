import sys
import subprocess

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Usage: python install_keyboard.py keyboard.klc')
        sys.exit()
    
    keyboard_file = sys.argv[1]
    keyboard_name = keyboard_file[:keyboard_file.find('.')]

    # Build AMD64 DLL
    rtn = subprocess.call(["bin\i386\kbdutool.exe", "-m", "{}".format(keyboard_file)])
    if rtn != 0:
        print('Build failed!  Exiting...')
        sys.exit()

    # Move file
    rtn = subprocess.call("move {}.dll C:\Windows\System32".format(keyboard_name), shell=True)
    if rtn != 0:
        print('Move failed! Try running in Administrator Mode...')
        sys.exit()

    # Build WOW64 DLL
    rtn = subprocess.call(["bin\i386\kbdutool.exe", "-o", "{}".format(keyboard_file)])
    if rtn != 0:
        print('Build failed!  Exiting...')
        sys.exit()

    # Move file
    rtn = subprocess.call("move {}.dll C:\Windows\SysWOW64".format(keyboard_name), shell=True)
    if rtn != 0:
        print('Move failed! Try running in Administrator Mode...')
        sys.exit()

    # TODO: Add register file
