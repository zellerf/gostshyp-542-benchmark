#!/usr/bin/python
import sys

# read final SCF energy from file specified by argv and print positions
def main():
    # get inputfile
    filename = str(sys.argv[1])

    # parse for SCF energy
    energy = parse_energy(filename)

    print(energy)
    return 0

def parse_energy(filename):
    converged = False
    energy = []

    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                if 'Final energy is' in line:
                    try:
                        splitline = line.split()
                        energy.append(float(splitline[3]))
                    except IOError:
                        print('Error while reading energy in ' + filename)
                        exit(1)
                if "OPTIMIZATION CONVERGED" in line:
                    converged = True
    except IOError:
        print('cannot open ' + filename)

    if len(energy) != 1:
        print('multiple calculations detected in ' + filename)
        exit(1)
    if converged == False:
        print('unconverged calculation in ' + filename)
        exit(1)

    return energy[0]

if __name__ == '__main__':
    exit(main())
