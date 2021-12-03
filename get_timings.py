import sys

# returns list of SCF timings / SCF cycles

def parse_scf_timings(filename):
    scf_times, scf_cylces = [], []
    input_detected, calc_finished = 0, 0

    try:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                if 'User input:' in line:
                    input_detected += 1
                if 'Thank you very much for using Q-Chem.  Have a nice day.' in line:
                    calc_finished += 1
                if 'Convergence criterion met' in line:
                    try:
                        splitline = line.split()
                        print(splitline)
                        scf_cylces.append(int(splitline[0]))
                    except IOError:
                        print('Error while reading SCF cycles ' + filename)
                        exit(1)
                if 'SCF time:' in line:
                    try:
                        splitline = line.split()
                        scf_times.append(float(splitline[3].strip('s')))
                    except IOError:
                        print('Error while reading SCF times in ' + filename)
                        exit(1)

    except IOError:
        print('cannot open ' + filename)
        exit(1)

    if input_detected != 1:
        print('Error: multiple calcs detected in ' + filename)
        exit(1)
    if calc_finished != 1:
        print('Error: crashed calculation in ' + filename)
        exit(1)
    if len(scf_times) != len(scf_cylces):
        print('Error: bad data detected in ' + filename + ' while reading SCF timings')
        exit(1)

    timings = []
    for i in range(len(scf_times)):
        timings.append(scf_times[i]/scf_cylces[i])

    return timings


def main():
    filename = sys.argv[1]
    scf_timings = parse_scf_timings(filename)
    print('SCF times /ncycles:')
    for i in scf_timings:
        print(i)

    return 0

if __name__ == '__main__':
    exit(main())
