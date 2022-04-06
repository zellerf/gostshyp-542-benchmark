#!/usr/bin/python
import sys


# read final SCF energy from file specified by argv and print
def main():
    # get inputfile
    filename = str(sys.argv[1])

    # parse for SCF energy
    energy = parse_energy(filename)

    print(energy)
    return 0


# Parse file with geometry optimization for final Energy
# filename[in]: string with filename
# energy[return]: Final energy in Hartrees
def parse_energy(filename):

    converged = False
    energy = []

    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                # get energy
                if 'Final energy is' in line:
                    splitline = line.split()
                    try:
                        energy.append(float(splitline[3]))
                    except ValueError:
                        print('Error while reading energy in ' + filename)
                        sys.exit(1)
                # check if converged
                if "OPTIMIZATION CONVERGED" in line:
                    converged = True
    except OSError:
        print('Error while reading energy: cannot open ' + filename)
        sys.exit(1)

    # check for multiple calculations and unconverged optimization
    if len(energy) != 1:
        print('multiple calculations detected in ' + filename)
        sys.exit(1)

    if not converged:
        print('Error while reading energy: unconverged calculation in ' + filename)
        sys.exit(1)

    return energy[0]


if __name__ == '__main__':
    sys.exit(main())
