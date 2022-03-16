import sys
import matplotlib.pyplot as plt

def plot_scf_times(out, ref):
    # check input parameters for correct data type
    if not isinstance(out, dict):
        print('passed wrong argument to function plot_energy')
        sys.exit(1)
    if not isinstance(ref, dict):
        print('passed wrong argument to function plot_energy')
        sys.exit(1)

    # read data from dicts
    out_nbsf, out_scf_times = [], []
    ref_nbsf, ref_scf_times = [], []
    # ref and out need to have the same keylist!
    for key in out.keys():
        try:
            out_nbsf.append(int(out[key]['nbsf']))
            # energy difference between out and reference
            out_scf_times.append(float(out[key]['scf_time'][0]))
            ref_nbsf.append(int(ref[key]['nbsf']))
            # energy difference between out and reference
            ref_scf_times.append(float(ref[key]['scf_time'][0]))
        except (KeyError, ValueError, TypeError, IndexError):
            print('Error: bad data detected while plotting scf-times')
            sys.exit(1)

    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_nbsf, out_scf_times, label='Q-Chem 5.4.2-dev', s=3)
    ref_times.scatter(ref_nbsf, ref_scf_times, label='Q-Chem 5.4.1', s=3)
    plt.xlabel("number of basis functions")
    plt.ylabel("SCFtime/ncycles [CPUs]")
    plt.legend()
    fig.savefig("scf_times.pdf")