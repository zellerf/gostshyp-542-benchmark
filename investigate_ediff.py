import sys
import os
import matplotlib.pyplot as plt


def parse_file(filename):
    cycles, energy = [], []
    try:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                if 'Convergence criterion met' in line:
                    try:
                        cycles.append(float(line.split()[0]))
                        energy.append(float(line.split()[1]))
                    except ValueError:
                        print('Error while checking ' + filename + 'for Energy difference')
                        sys.exit(1)
    except IOError:
        print('Error: could not open ' + filename)
        sys.exit(1)
    return energy, cycles


def plot_scf_diff(name):
    # TODO check if string
    out_energies, out_cycles = [], []
    ref_energies, ref_cycles = [], []
    for root, subdirs, files in os.walk(os.getcwd()):
        for file in files:
            # read out files
            if file == name + '.out':
                if out_energies or out_cycles:
                    print('Error: multiple copies of ' + name + '.out')
                out_energies, out_cycles = parse_file(root + '/' + name +'.out')
            if file == name + '.ref':
                if ref_energies or ref_cycles:
                    print('Error: multiple copies of ' + name + '.ref')
                ref_energies, ref_cycles = parse_file(root + '/' + name +'.ref')

    fig = plt.figure()
    energy = plt.subplot()
    energy.plot(out_energies, label='Q-Chem 5.4.2-dev', marker='x')
    energy.plot(ref_energies, label='Q-Chem 5.4.1', marker='x')
    plt.xlabel("Optimization cycle")
    plt.ylabel("$E$ [Hartree]")
    plt.legend()
    fig.savefig(name + ".pdf")


def main():
    filename = sys.argv[1]
    plot_scf_diff(filename)
    return 0


if __name__ == '__main__':
    sys.exit(main())
