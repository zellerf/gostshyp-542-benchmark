import sys
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


def plot_memusage(out, ref):
    # check input parameters for correct data type
    if not isinstance(out, dict):
        print('passed wrong argument to function plot_memusage')
        sys.exit(1)
    if not isinstance(ref, dict):
        print('passed wrong argument to function plot_memusage')
        sys.exit(1)

    # read data from dicts
    out_ntess, out_nbsf, out_mem = [], [], []
    ref_ntess, ref_nbsf, ref_mem = [], [], []
    # ref and out need to have the same keylist!
    for key in out.keys():
        try:
            out_ntess.append(int(out[key]['ntess']))
            ref_ntess.append(int(ref[key]['ntess']))
            out_nbsf.append(int(out[key]['nbsf']))
            ref_nbsf.append(int(ref[key]['nbsf']))
            out_mem.append(float(out[key]['mem']))
            ref_mem.append(calc_ref_mem(ref_nbsf[-1], ref_ntess[-1]))
        except (KeyError, ValueError, TypeError, IndexError):
            print('Error: bad data detected while plotting mem_usage')
            sys.exit(1)

    # linear regression
    x_out, y_out = np.array(out_ntess), np.array(out_mem)
    x_out = x_out.reshape(-1, 1)
    model_out = LinearRegression()
    model_out.fit(x_out, y_out)

    print("Performing linear regression of gostshyp static mem to number of tesserae")
    print("Q-Chem 5.4.2 y-intercept:", model_out.intercept_)
    print("Q-Chem 5.4.2 Steigung:", model_out.coef_)
    print("Q-Chem 5.4.2 R²:", model_out.score(x_out, y_out))

    # points to draw regression line
    t = (max(x_out), min(x_out))

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_ntess, out_mem, label='Q-Chem 5.4.2-dev', s=3)
    out_times.plot(t, model_out.predict(t))
    ref_times.scatter(ref_ntess, ref_mem, label='Q-Chem 5.4.1', s=3)
    plt.xlabel("number of tesserae")
    plt.ylabel("maximum mem usage [MB]")
    plt.legend()
    fig.savefig("mem_ntess.pdf")
    plt.close(fig)

    # quadratic regression
    x_out, y_out = np.array(out_nbsf), np.array(out_mem)
    x_out = x_out.reshape(-1, 1)
    model_out = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model_out.fit(x_out, y_out)

    print("Performing quadratic regression of mem usage to number of basis functions")
    print("Q-Chem 5.4.2 y-intercept:", model_out.named_steps['linearregression'].intercept_)
    print("Q-Chem 5.4.2 coeffs:", model_out.named_steps['linearregression'].coef_)
    print("Q-Chem 5.4.2 R²:", model_out.score(x_out, y_out))

    # create data points to plot regression data
    x_outseq = np.linspace(x_out.min(), x_out.max(), 500).reshape(-1, 1)

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_nbsf, out_mem, label='Q-Chem 5.4.2-dev', s=3)
    out_times.plot(x_outseq, model_out.predict(x_outseq))
    ref_times.scatter(ref_nbsf, ref_mem, label='Q-Chem 5.4.1', s=3)
    plt.xlabel("number of basis functions")
    plt.ylabel("maximum mem usage [MB]")
    plt.legend()
    fig.savefig("mem_nbsf.pdf")
    plt.close(fig)

# max mem usage is easily calculatable for old implementation, since the overlap matrices are not sparse
# max mem usage = nbsf ** 2 * ntess * 5 * sizeof(double)
# return mem usage in MB
def calc_ref_mem(nbsf, ntess):
    return nbsf ** 2 * ntess * 40 / (1024 * 1024)
