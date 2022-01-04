import sys


def check_convergence(filename):
    conv_counter = 0
    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                if 'OPTIMIZATION CONVERGED' in line:
                    conv_counter += 1
    except IOError:
        print('Error while opening ' + filename)
        sys.exit(1)
    if conv_counter != 1:
        return False
    return True

def main():
    filename = sys.argv[1]
    if check_convergence(filename):
        print(filename + ' is converged')
    else:
        print(filename + ' is not converged')
    return 0


if __name__ == '__main__':
    sys.exit(main())