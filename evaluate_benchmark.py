# This is the main function!
import os, sys
import statistics
import get_nbsf
import get_geometry
import get_timings
import get_energy


# read data from input file, digest and save in return value
# filename[in] name of file to extract data from
# data[return] dict containing keys:
#   "energy" [float] final energy of optimized geometry
#   "nbsf" [int] number of basis functions
#   "grad_time" [float, float] average calculation time for gradient, standard deviation
#   "scf_time" [float, float] average SCF calc time / SCF cycles, standard deviation
#   "geometry" [list of floats] final geometry of molecule in xyz coordinates
def read_file(filename):
    data = {}
    # read energy
    try:
        data['energy'] = get_energy.parse_energy(filename)
    except IOError:
        print("Error while reading " + filename + " for energy.")
        exit(1)

    # read geometry
    try:
        data['geometry'] = get_geometry.parse_xyz(filename)
    except IOError:
        print("Error while reading " + filename + " for geometry.")

    # get SCF timings
    try:
        scf = get_timings.parse_scf_timings(filename)
        data['scf_time'] = [statistics.mean(scf), statistics.stdev(scf)]
    except IOError:
        print("Error while reading " + filename + " for SCF timings.")

    # get gradient timings
    try:
        grad = get_timings.parse_grad_times(filename)
        data['grad_time'] = [statistics.mean(grad), statistics.stdev(grad)]
    except IOError:
        print("Error while reading " + filename + " for gradient timings.")

    # get number of basis functions
    try:
        data['nbsf'] = get_nbsf.parse_nbsf(filename)
    except IOError:
        print("Error while reading " + filename + " for number of basis functions.")

    return data


def main():
    out ={} # dict containing data of all out files
    ref = {} # dict containing data of all ref files

    # parse recursively through all folders/files in current working directory and read data in out/ref
    for root, subdirs, files in os.walk(os.getcwd()):
        for file in files:
            # read out files
            if file.startswith('.out'):
                # use filename as key
                key = file.strip('.out')
                # check for multiple copies
                if key in out.keys():
                    print('Error: multiple copies of ' + file)
                    sys.exit(1)
                else:
                    try:
                        out[key] = read_file(file)
                    except IOError:
                        print('Error while reading data from ' + file)
                        sys.exit(1)

            # read ref files
            if file.startswith('.ref'):
                # use filename as key
                key = file.strip('.ref')
                # check for multiple copies
                if key in ref.keys():
                    print('Error: multiple copies of ' + file)
                    sys.exit(1)
                else:
                    try:
                        ref[key] = read_file(file)
                    except IOError:
                        print('Error while reading data from ' + file)
                        sys.exit(1)

    # check that there were as many .ref files as .out
    if len(out.keys()) != len(ref.keys()):
        print('Number of reference calcs does not match number of calcs.')
        sys.exit(1)
    for key in out.keys():
        if key not in ref.keys():
            print('There are .out calcs without .ref calc.')
            sys.exit(1)

    #plot

    return 0


if __name__ == '__main__':
    exit(main())

