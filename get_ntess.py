#!/usr/bin/python
import sys
import numpy as np

# read number of average kept tesserae from file specified by argv and print positions
def main():
    # get inputfile
    filename = str(sys.argv[1])

    # parse for SCF energy
    ntess = parse_ntess(filename)

    print('average number of kept tesserae in calculation:')
    print(ntess)
    return 0


# Parse file with geometry optimization for number of kept tesserae
# filename[in]: string with filename
# ntess [return]: number of tesserae
def parse_ntess(filename):

    converged = 0
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
                # check if converged
                if "OPTIMIZATION CONVERGED" in line:
                    converged += 1
    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    # check if several numbers of basis functions were detected
    # -> this is a workaround for a multiple calculations check, since Qchem prints nbsf each optimization cycle
    if converged != 1:
        print('Error: unconverged calculation in ' + filename)
        sys.exit(1)

    return int(np.average(ntess))

if __name__ == '__main__':
    sys.exit(main())