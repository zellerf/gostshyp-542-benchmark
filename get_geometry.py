#!/usr/bin/python
import sys

# read molecular positions from file specified by argv and print positions
def main():
    # get inputfile
    coordfile = str(sys.argv[1])

    # parse for converged geometry
    coordinates = parse_xyz(coordfile)

    # print coordinates format
    for coord in coordinates:
        print(str("%.8f" % coord[0]) + ' ' + str("%.8f" % coord[1]) + ' ' + str("%.8f" % coord[2]))
    return 0


# parse specified file for converged geometry
# file[in]: filename zo parse
# coordinates[return]: list of xyz coordinates
def parse_xyz(file):
    coordinates = []
    opt_conv = []
    try:
        with open(file) as ifile:
            lines = ifile.readlines()
            for line in lines:
                if "OPTIMIZATION CONVERGED" in line:
                    opt_conv.append(lines.index(line))
            if len(opt_conv) != 1:
                print('unconverged geometry or multiple jobs in ' + file)
                exit(1)
            for line in lines[opt_conv[0]:]:
                if 'Z-matrix Print:' in line:
                    break
                splitline = line.split()
                if len(splitline) != 5:
                    continue
                try:
                    coordinates.append([float(splitline[2]), float(splitline[3]), float(splitline[4])])
                except IOError:
                    print('Error while reading xyz geometry!')
                    exit(1)
    except IOError:
        print('could not open ' + file)
        exit(1)
    ifile.close()
    return coordinates


if __name__ == '__main__':
    exit(main())
