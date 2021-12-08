# This is the main function!
import os, sys
import statistics
import get_nbsf
import get_geometry
import get_timings
import get_energy
import plots

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
    data['energy'] = get_energy.parse_energy(filename)

    # read geometry
    data['geometry'] = get_geometry.parse_xyz(filename)


    # get SCF timings
    scf = get_timings.parse_scf_timings(filename)
    data['scf_time'] = [statistics.mean(scf), statistics.stdev(scf)]

    # get gradient timings
    grad = get_timings.parse_grad_times(filename)
    data['grad_time'] = [statistics.mean(grad), statistics.stdev(grad)]

    # get number of basis functions
    data['nbsf'] = get_nbsf.parse_nbsf(filename)

    return data


def main():
    out ={} # dict containing data of all out files
    ref = {} # dict containing data of all ref files

    # parse recursively through all folders/files in current working directory and read data in out/ref
    for root, subdirs, files in os.walk(os.getcwd()):
        for file in files:
            # read out files
            if file.endswith('.out'):
                # use filename as key
                key = file.removesuffix('.out')
                # check for multiple copies
                if key in out.keys():
                    print('Error: multiple copies of ' + file)
                    sys.exit(1)
                else:
                    out[key] = read_file(root + '/' + file)

            # read ref files
            if file.endswith('.ref'):
                # use filename as key
                key = file.removesuffix('.ref')
                # check for multiple copies
                if key in ref.keys():
                    print('Error: multiple copies of ' + file)
                    sys.exit(1)
                else:
                    ref[key] = read_file(root + '/' + file)

    # check that there were as many .ref files as .out
    if len(out.keys()) != len(ref.keys()):
        print('Number of reference calcs does not match number of calcs.')
        sys.exit(1)
    for key in out.keys():
        if key not in ref.keys():
            print('There are .out calcs without .ref calc.')
            sys.exit(1)

    #plot
    plots.plot_energy(out, ref)

    return 0


if __name__ == '__main__':
    exit(main())

