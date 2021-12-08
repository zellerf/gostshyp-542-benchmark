#!/usr/bin/python
import sys


# read number of basis functions from file specified by argv and print positions
def main():
    # get inputfile
    filename = str(sys.argv[1])

    # parse for SCF energy
    nbsf = parse_nbsf(filename)

    print('number of basis functions in file:')
    print(nbsf)
    return 0


# Parse file with geometry optimization for number of basis functions
# filename[in]: string with filename
# nbsf [return]: number of basis functions
def parse_nbsf(filename):

    converged = False
    nbsf = []

    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                # get nbsf
                if 'basis functions' in line:
                    splitline = line.split()
                    try:
                        nbsf.append(int(splitline[5]))
                    except ValueError:
                        print('Error while reading number of basis functions from ' + filename)
                        sys.exit(1)
                # check if converged
                if "OPTIMIZATION CONVERGED" in line:
                    converged = True
    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    # check if several numbers of basis functions were detected
    # -> this is a workaround for a multiple calculations check, since Qchem prints nbsf each optimization cycle
    if sum(nbsf) / len(nbsf) != nbsf[0]:
        print('multiple calculations detected in ' + filename)
        sys.exit(1)

    return nbsf[0]

if __name__ == '__main__':
    sys.exit(main())