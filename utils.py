import os
import sys

NAME_PROTOCOL = os.path.basename(sys.argv[0])[:-3]


def read(filename):
    with open(os.path.join('files_' + NAME_PROTOCOL, filename)) as f:
        return int(f.read())


def read_arr(*filenames):
    return (read(arg) for arg in filenames)


def write(filename, value):
    with open(os.path.join('files_' + NAME_PROTOCOL, filename), 'w') as f:
        f.write(str(value))
