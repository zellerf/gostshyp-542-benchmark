# script to read gostshyp mem static from file
# needs specifically modified gostshypversion that prints mem static

import sys


# read static mem usage of gostshyp during each optimization cycle
def main():
    # get file input
    filename = str(sys.argv[1])

    # parse for mem_usage
    mem_static = parse_mem_static(filename)

    print('mem_static used by gostshyp in MB calculation:')
    print(mem_static)
    return 0


# Parse file for mem_static usage
# filename[in]: string with filename
# mem_static [return]: mem_static for each opt cycle in MB
def parse_mem_static(filename):
    mem_static = []
    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                # get mem usage during SCF cycle
                if 'gostshyp mem_static in MB: ' in line:
                    splitline = line.split()
                    try:
                        mem_static.append(float(splitline[4]))
                    except ValueError:
                        print('Error while reading gosthsyp mem static usage from ' + filename)
                        sys.exit(1)
    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    return mem_static


if __name__ == '__main__':
    sys.exit(main())
