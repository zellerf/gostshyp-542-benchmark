import sys
import matplotlib.pyplot as plt
import numpy as np

# function to plot maximum molecular displacement vs number of basis functions
# out[in] dict with data of benchmark calculations
# ref[in] dict with data of reference calculations
def plot_displacement(out, ref):
    # check input parameters for correct data type
    if not isinstance(out, dict):
        print('passed wrong argument to function plot_displacement')
        sys.exit(1)
    if not isinstance(ref, dict):
        print('passed wrong argument to function plot_displacement')
        sys.exit(1)

    # read data from dicts
    nbsf = [] # number of basis functions
    displacement = [] # maximum displacement in each calculation

    # ref and out need to have the same keylist!
    for key in out.keys():
        try:
            nbsf.append(int(out[key]['nbsf']))
            max_displ = calc_displacement(np.array(out[key]['geometry']), np.array(ref[key]['geometry']))
            displacement.append(max_displ)
        except (KeyError, ValueError, TypeError, IndexError):
            print('Error: bad data detected while plotting displacement')
            sys.exit(1)

    # plot
    fig = plt.figure()
    displ = plt.subplot()
    # draw dotted line at displacement convergence criterium
    displ_conv = plt.subplot()
    displ_thresh = [1200 * 1e-6]*len(nbsf)
    displ_conv.plot(nbsf, displ_thresh, linestyle='dashed', marker='')
    displ.scatter(nbsf, displacement, marker='x')
    displ_conv.set_yscale('log')
    displ.set_yscale('log')
    plt.xlabel("number of basis functions")
    plt.ylabel("max displacement [$\mathring{A}$]")
    fig.savefig("displacement.pdf")
    plt.cla()
    plt.clf()

# calculates the maximum displacement between a benchmark calc and a reference calc
# out_geom[in] np array with data of benchmark calculations
# ref_geom[in] np array with data of reference calculations
# return max displacement
def calc_displacement(out_geom, ref_geom):
    # check input parameters for correct data type
    if not isinstance(out_geom, np.ndarray):
        print('passed wrong argument to unction calculatuing displacement')
        sys.exit(1)
    if not isinstance(ref_geom, np.ndarray):
        print('passed wrong argument to function calculatuing displacement')
        sys.exit(1)

    try:
        diff = out_geom - ref_geom
    except (KeyError, ValueError, TypeError, IndexError):
        print('Error: bad data detected while calculating displacement')
        sys.exit(1)

    max_displacement = 0
    for i in diff:
        # length of diff vector
        displacement = np.sqrt(i[0]**2 + i[1]**2 + i[2]**2)
        if displacement > max_displacement:
            max_displacement = displacement
    return max_displacement
