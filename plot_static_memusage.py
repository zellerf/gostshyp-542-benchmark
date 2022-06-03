import sys
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import split_dataset


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

    # split into training and test sets
    out_ntess_train, out_ntess_test = split_dataset.split_dataset(out_ntess)
    out_nbsf_train, out_nbsf_test = split_dataset.split_dataset(out_nbsf)
    out_mem_train, out_mem_test = split_dataset.split_dataset(out_mem)

    # linear regression
    x_out, y_out = np.array(out_ntess_train), np.array(out_mem_train)
    x_out = x_out.reshape(-1, 1)
    model_out = LinearRegression()
    model_out.fit(x_out, y_out)

    # rmse
    x_test = np.array(out_ntess_test)
    x_test = x_test.reshape(-1, 1)
    y_test = model_out.predict(x_test)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, out_mem_test))

    # print metrics
    print("Performing linear regression of gostshyp static mem to number of tesserae")
    print("Q-Chem 5.4.2 y-intercept:", model_out.intercept_)
    print("Q-Chem 5.4.2 Steigung:", model_out.coef_)
    print("Q-Chem 5.4.2 R²:", model_out.score(x_out, y_out))
    print("Q-Chem 5.4.2 RMSE:", rmse)

    # draw regression line
    x = np.linspace(min(out_ntess), max(out_ntess), 500)
    y = model_out.predict(x.reshape(-1, 1))

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_ntess, out_mem, label='Q-Chem 5.4.2-dev', s=3, color='#1B2ACC')
    out_times.plot(x, y, color='#1B2ACC')
    out_times.fill_between(x, y-rmse, y+rmse, alpha=0.25, edgecolor='#1B2ACC', facecolor='#089FFF')
    ref_times.scatter(ref_ntess, ref_mem, label='Q-Chem 5.4.1', s=3, color='#CC4F1B')
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
