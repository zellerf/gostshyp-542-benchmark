import sys
import investigate_ediff
import matplotlib.pyplot as plt
import numpy as np


def plot_energy(out, ref):
    # check input parameters for correct data type
    if not isinstance(out, dict):
        print('passed wrong argument to function plot_energy')
        sys.exit(1)
    if not isinstance(ref, dict):
        print('passed wrong argument to function plot_energy')
        sys.exit(1)

    # read data from dicts
    nbsf, energies = [], []
    for key in out.keys():
        try:
            nbsf.append(int(out[key]['nbsf']))
            # energy difference between out and reference
            if abs(float(out[key]['energy'] - ref[key]['energy'])) > 10e-6:
                # TODO move in general part
                investigate_ediff.plot_scf_diff(key)
            energies.append(abs(float(out[key]['energy'] - ref[key]['energy'])))
        except (KeyError, ValueError, TypeError):
            print('Error while digesting energies')
            sys.exit(1)

    fig = plt.figure()
    ediff = plt.subplot()
    scf_conv = plt.subplot()
    # add dashed line for SCF convergence thresh
    geoopt_thresh = [1e-6]*len(nbsf)
    scf_conv.plot(nbsf, geoopt_thresh, marker='')
    ediff.scatter(nbsf, energies, label='$\Delta E$', marker='x')
    scf_conv.set_yscale('log')
    scf_conv.set_ylim(1e-16, 1e-2)
    ediff.set_yscale('log')
    plt.xlabel("number of basis functions")
    plt.ylabel("$\Delta E$ [Hartree]")
    fig.savefig("energies.pdf")
