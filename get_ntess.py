#!/usr/bin/python
import sys
import numpy as np


# read number of average kept tesserae from file specified by argv and print positions
def main():
    # get inputfile
    filename = str(sys.argv[1])

    # parse for tesserae
    ntess = parse_ntess(filename)

    print('average number of kept tesserae in calculation:')
    print(ntess)
    return 0


# Parse file for number of kept tesserae
# filename[in]: string with filename
# ntess [return]: number of tesserae
def parse_ntess(filename):

    ntess = []
    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                # get ntess
                if 'surface tesserae' in line:
                    splitline = line.split()
                    try:
                        ntess.append(int(splitline[1]))
                    except ValueError:
                        print('Error while reading number of basis functions from ' + filename)
                        sys.exit(1)
    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    # convert to int
    return int(np.average(ntess))


if __name__ == '__main__':
    sys.exit(main())