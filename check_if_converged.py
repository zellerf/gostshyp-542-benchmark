import sys

# will return 0 if file contains a sucessful calculation
# returns an error code otherwise
# Error codes:
# -1 unknown error
# 1 multiple calculations detected
# 2 max SCF cycles reached
# 3 max optimization cycles reached

def check_convergence(filename):
    conv_counter = 0
    error_code = 0
    try:
        with open(filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                if 'Thank you very much for using Q-Chem.  Have a nice day' in line:
                    conv_counter += 1
                if 'gen_scfman_exception: SCF failed to converge' in line:
                    error_code = 2
                if 'Maximum optimization cycles reached' in line:
                    error_code = 3
    except IOError:
        print('Error while opening ' + filename)
        sys.exit(1)
    if conv_counter == 1 and error_code == 0:
        return 0
    if conv_counter > 1:
        return 1
    if conv_counter == 0 and error_code == 0:
        return -1
    return error_code


# evaluate errorcode from check_convergence
def evaluate_errcode(errorcode):
    if errorcode == 0:
        print('calculation converged successfully')
    elif errorcode == 1:
        print('multiple calculations detected, unable to process')
    elif errorcode == 2:
        print('maximum scf cycles reached')
    elif errorcode == 3:
        print('maximum optimizations reached')
    else:
        print('calculation failed due to unknown error')


def main():
    filename = sys.argv[1]
    evaluate_errcode(check_convergence(filename))


if __name__ == '__main__':
    sys.exit(main())