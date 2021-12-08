import sys
import matplotlib.pyplot as plt


def plot_grad_times(out, ref):
    # check input parameters for correct data type
    if not isinstance(out, dict):
        print('passed wrong argument to function plot_energy')
        sys.exit(1)
    if not isinstance(ref, dict):
        print('passed wrong argument to function plot_energy')
        sys.exit(1)

    # read data from dicts
    out_nbsf, out_grad_times, out_error = [], [], []
    ref_nbsf, ref_grad_times, ref_error = [], [], []
    # ref and out need to have the same keylist!
    for key in out.keys():
        try:
            out_nbsf.append(int(out[key]['nbsf']))
            # energy difference between out and reference
            out_grad_times.append(float(out[key]['grad_time'][0]))
            out_error.append(float(out[key]['grad_time'][1]))
            ref_nbsf.append(int(ref[key]['nbsf']))
            # energy difference between out and reference
            ref_grad_times.append(float(ref[key]['grad_time'][0]))
            ref_error.append(float(ref[key]['grad_time'][1]))
        except (KeyError, ValueError, TypeError, IndexError):
            print('Error: bad data detected while plotting scf-times')
            sys.exit(1)

    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    #out_times.scatter(out_nbsf, out_scf_times, label='screened', marker='o')
    out_times.errorbar(out_nbsf, out_grad_times, yerr=out_error,
                       label='screened', fmt='.', markersize='5', capsize=2)
    ref_times.errorbar(ref_nbsf, ref_grad_times, yerr=ref_error,
                       label='unscreened', fmt='.', markersize='5', capsize=2)
    #out_times.set_yscale('log')
    #ref_times.set_yscale('log')
    plt.xlabel("number of basis functions")
    plt.ylabel("grad time/ncycles [CPUs]")
    plt.legend()
    fig.savefig("grad_times.pdf")