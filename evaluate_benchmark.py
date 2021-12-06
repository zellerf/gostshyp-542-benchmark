# This is the main function!
import statistics
import get_nbsf
import get_geometry
import get_timings
import get_energy

if __name__ == '__main__':
    exit(main())

def main():
    
    return 0

# read data from input file, digest and save in return value
# filename[in] name of file to extract data from
# data[return] dict containing keys:
#   "energy" [float] final energy of optimized geometry
#   "nbsf" [int] number of basis functions
#   "gradient_timing" [float, float] average calculation time for gradient, standard deviation
#   "scf_timings" [float, float] average SCF calc time / SCF cycles, standard deviation
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
        data['scf_timings'] = [statistics.mean(scf), statistics.stdev(scf)]
    except IOError:
        print("Error while reading " + filename + " for SCF timings.")

    # get gradient timings
    try:
        grad = get_timings.parse_grad_times(filename)
        data['gradient_timings'] = [statistics.mean(grad), statistics.stdev(grad)]
    except IOError:
        print("Error while reading " + filename + " for gradient timings.")

    # get number of basis functions
    try:
        data['nbsf'] = get_nbsf.parse_nbsf(filename)
    except IOError:
        print("Error while reading " + filename + " for number of basis functions.")
    return data