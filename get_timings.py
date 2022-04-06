import sys


# parses file fo scf times in CPU seconds scaled with number of corresponding SCF cycles
# filename[in]: string, name of file to parse
# timings[return] list of CPUs /ncycles
def parse_scf_timings(filename):
    scf_times, scf_cylces = [], []
    # counters for number of input files detected and for finished calcs, only for error detection
    input_detected, calc_finished = 0, 0

    try:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                # check file if only contains ONE finished calculation
                if 'User input:' in line:
                    input_detected += 1
                if 'Thank you very much for using Q-Chem.  Have a nice day.' in line:
                    calc_finished += 1
                # get number of scf cycles in of this SCF
                if 'Convergence criterion met' in line:
                    splitline = line.split()
                    try:
                        scf_cylces.append(int(splitline[0]))
                    except ValueError:
                        print('Error while reading SCF cycles ' + filename)
                        sys.exit(1)
                # get SCF time
                if 'SCF time:' in line:
                    splitline = line.split()
                    try:
                        scf_times.append(float(splitline[3].strip('s')))
                    except ValueError:
                        print('Error while reading SCF times in ' + filename)
                        sys.exit(1)

    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    # crash if file didnt contain only one calc or was crashed
    if input_detected != 1:
        print('Error: multiple calcs detected in ' + filename)
        sys.exit(1)
    if calc_finished != 1:
        print('Error: crashed calculation in ' + filename)
        sys.exit(1)
    if len(scf_times) != len(scf_cylces):
        print('Error: bad data detected in ' + filename + ' while reading SCF timings')
        sys.exit(1)

    # calc SCF time per SCF cycle for each SCF
    timings = []
    for i in range(len(scf_times)):
        timings.append(scf_times[i] / scf_cylces[i])

    return timings


# parses file fo gradient times in CPU seconds
# filename[in]: string, name of file to parse
# timings[return] list of gradient times in CPUs
def parse_grad_times(filename):
    grad_times = []
    # counters for number of input files detected and for finished calcs, only for error detection
    input_detected, calc_finished = 0, 0

    try:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                # check if file only contains ONE finished calculation
                if 'User input:' in line:
                    input_detected += 1
                if 'Thank you very much for using Q-Chem.  Have a nice day.' in line:
                    calc_finished += 1
                # get grad time
                if ' Gradient time:' in line:
                    splitline = line.split()
                    try:
                        grad_times.append(float(splitline[3].strip('s')))
                    except ValueError:
                        print('Error while reading gradient times from ' + filename)
                        sys.exit(1)

    except OSError:
        print('cannot open ' + filename)
        sys.exit(1)

    # crash if file did not contain only one calc or was crashed
    if input_detected != 1:
        print('Error: multiple calcs detected in ' + filename)
        sys.exit(1)
    if calc_finished != 1:
        print('Error: crashed calculation in ' + filename)
        sys.exit(1)

    return grad_times


def main():
    filename = sys.argv[1]

    # get SCF times
    scf_timings = parse_scf_timings(filename)
    print('SCF times /ncycles [CPUs]:')
    for i in scf_timings:
        print(i)

    # get Grad times
    grad_timings = parse_grad_times(filename)
    print('Gradient times [CPUs]')
    for i in grad_timings:
        print(i)
    return 0


if __name__ == '__main__':
    sys.exit(main())
