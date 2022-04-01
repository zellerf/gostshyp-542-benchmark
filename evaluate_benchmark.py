# This is the main function!
import os
import statistics
import sys

# import get functions to read files
import get_energy
import get_geometry
import get_nbsf
import get_timings
import check_if_converged
import get_ntess
import get_memstatic

# import plotting scripts
import plot_displacement
import plot_enrgies
import plot_grad_times
import plot_scf_times
import plot_static_memusage

# read data from input file, digest and save in return value
# filename[in] name of file to extract data from
# data[return] dict containing keys:
#   "energy" [float] final energy of optimized geometry
#   "nbsf" [int] number of basis functions
#   "grad_time" [float, float] average calculation time for gradient, standard deviation
#   "scf_time" [float, float] average SCF calc time / SCF cycles, standard deviation
#   "geometry" [list of floats] final geometry of molecule in xyz coordinates
def read_file(filename, plotmem):

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

    # get average number of tesserae
    data['ntess'] = get_ntess.parse_ntess(filename)

    # get avarage mem static
    if plotmem:
        mem = get_memstatic.parse_mem_static(filename)
        data['mem'] = statistics.mean(mem)

    return data


def main():
    plotmem = False
    if sys.argv [1] == "-plotmem=true":
        plotmem = True
        print("enabling memory evaluation")
    out = {}  # dict containing data of all out files
    ref = {}  # dict containing data of all ref files
    crashed_out, crashed_ref = [], []
    err_max_scf, err_max_opt, err_unkown = 0, 0, 0 # counters for different eror codes
    # parse recursively through all folders/files in current working directory and read data in out/ref
    for root, subdirs, files in os.walk(os.getcwd()):
        # screen for crashed calcs and to lists
        for file in files:
            if file.endswith('.out') or file.endswith('.ref'):
                error = check_if_converged.check_convergence(root + '/' + file)
                if file.endswith('.out') and error != 0:
                    crashed_out.append(file.removesuffix('.out'))
                elif file.endswith('.ref') and error != 0:
                    crashed_ref.append(file.removesuffix('.ref'))
                if error == -1:
                    err_unkown += 1
                if error == 2:
                    err_max_scf += 1
                if error == 3:
                    err_max_opt += 1

         # read data
        for file in files:
            # read out files
            if file.endswith('.out'):
                # use filename as key
                key = file.removesuffix('.out')
                # skip if .out or .ref calc did not converge
                if key in crashed_out or key in crashed_ref:
                    continue
                # check for multiple copies
                if key in out.keys():
                    print('Error: multiple copies of ' + file)
                    sys.exit(1)
                else:
                    out[key] = read_file(root + '/' + file, plotmem)

            # read ref files
            if file.endswith('.ref'):
                # use filename as key
                key = file.removesuffix('.ref')
                # skip if .out or .ref calc did not converge
                if key in crashed_out or key in crashed_ref:
                    continue
                # check for multiple copies
                if key in ref.keys():
                    print('Error: multiple copies of ' + file)
                    sys.exit(1)
                else:
                    # always pass plotmem false, since mem usage of ref can be calculated
                    ref[key] = read_file(root + '/' + file, False)

    # check that there were as many .ref files as .out
    if len(out.keys()) != len(ref.keys()):
        print('Number of reference calcs does not match number of calcs.')
        sys.exit(1)
    for key in out.keys():
        if key not in ref.keys():
            print('There are .out calcs without .ref calc.')
            sys.exit(1)

    # evaluate crashs
    single_crashs = set(crashed_out) ^ set(crashed_ref)
    print('total number of crashs: ' + str(len(crashed_out) + len(crashed_ref)))
    print('crashed Qchem 5.4.2 calcs: ' + str(len(crashed_out)))
    print('crashed Qchem 5.4.1 calcs: ' + str(len(crashed_ref)))
    print('calculations with only .ref or .out crashed:')
    for crash in single_crashs:
        print(crash)
    print('crashs due to max scf cycles reached: ' + str(err_max_scf))
    print('crashs due to max opt cycles reached: ' + str(err_max_opt))
    print('crashs due to unknown reason: ' + str(err_unkown))

    # plot
    plot_enrgies.plot_energy(out, ref)
    plot_scf_times.plot_scf_times(out, ref)
    plot_grad_times.plot_grad_times(out, ref)
    plot_displacement.plot_displacement(out, ref)
    if plotmem:
        plot_static_memusage.plot_memusage(out, ref)
    return 0


if __name__ == '__main__':
    exit(main())

