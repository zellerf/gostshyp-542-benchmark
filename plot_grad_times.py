import sys
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


def plot_grad_times(out, ref):

    # check input parameters for correct data type
    if not isinstance(out, dict):
        print('passed wrong argument to function plot_grad_times')
        sys.exit(1)
    if not isinstance(ref, dict):
        print('passed wrong argument to function plot_grad:times')
        sys.exit(1)

    # plot time vs ntess
    # read data from dicts
    out_ntess, out_grad_times= [], []
    ref_ntess, ref_grad_times= [], []
    # ref and out need to have the same keylist!
    for key in out.keys():
        try:
            out_ntess.append(int(out[key]['ntess']))
            out_grad_times.append(float(out[key]['grad_time'][0]))
            ref_ntess.append(int(ref[key]['ntess']))
            ref_grad_times.append(float(ref[key]['grad_time'][0]))
        except (KeyError, ValueError, TypeError, IndexError):
            print('Error: bad data detected while plotting grad-times')
            sys.exit(1)

    # linear regression
    x_out, y_out = np.array(out_ntess), np.array(out_grad_times)
    x_out = x_out.reshape(-1, 1)
    x_ref, y_ref = np.array(ref_ntess), np.array(ref_grad_times)
    x_ref = x_ref.reshape(-1, 1)
    model_ref = LinearRegression()
    model_ref.fit(x_ref, y_ref)
    model_out = LinearRegression()
    model_out.fit(x_out, y_out)

    print("Performing linear regression of gradient timings to number of tesserae")
    print("Q-Chem 5.4.1 y-intercept:", model_ref.intercept_)
    print("Q-Chem 5.4.1 slope:", model_ref.coef_)
    print("Q-Chem 5.4.1 R²:", model_ref.score(x_ref, y_ref))

    print("Q-Chem 5.4.2 y-intercept:", model_out.intercept_)
    print("Q-Chem 5.4.2 slope:", model_out.coef_)
    print("Q-Chem 5.4.2 R²:", model_out.score(x_out, y_out))

    # points to draw regression line
    t = (max(x_out), min(x_out))

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_ntess, out_grad_times, label='Q-Chem 5.4.2-dev', s=3)
    out_times.plot(t, model_out.predict(t))
    ref_times.scatter(ref_ntess, ref_grad_times, label='Q-Chem 5.4.1', s=3)
    ref_times.plot(t, model_ref.predict(t))
    plt.xlabel("number of tesserae")
    plt.ylabel("Time per gradient calculation [CPUs]")
    plt.legend()
    fig.savefig("grad_times_ntess.pdf")
    plt.close(fig)

    # plot vs nbsf
    out_nbsf, ref_nbsf = [], []
    for key in out.keys():
        try:
            out_nbsf.append(int(out[key]['nbsf']))
            ref_nbsf.append(int(ref[key]['nbsf']))
        except (KeyError, ValueError, TypeError, IndexError):
            print('Error: bad data detected while plotting scf-times')
            sys.exit(1)

    # quadratic regression
    x_out, y_out = np.array(out_nbsf), np.array(out_grad_times)
    x_out = x_out.reshape(-1, 1)
    x_ref, y_ref = np.array(ref_nbsf), np.array(ref_grad_times)
    x_ref = x_ref.reshape(-1, 1)
    model_ref = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model_ref.fit(x_ref, y_ref)
    model_out = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model_out.fit(x_out, y_out)

    print("Performing quadratic regression of gradient timings to number of basis functions")
    print("Q-Chem 5.4.1 y-intercept:", model_ref.named_steps['linearregression'].intercept_)
    print("Q-Chem 5.4.1 coeffs:", model_ref.named_steps['linearregression'].coef_)
    print("Q-Chem 5.4.1 R²:", model_ref.score(x_ref, y_ref))

    print("Q-Chem 5.4.2 y-intercept:", model_out.named_steps['linearregression'].intercept_)
    print("Q-Chem 5.4.2 coeffs:", model_out.named_steps['linearregression'].coef_)
    print("Q-Chem 5.4.2 R²:", model_out.score(x_out, y_out))

    # create data points to plot regression data
    x_outseq = np.linspace(x_out.min(),x_out.max(),500).reshape(-1,1)
    x_refseq = np.linspace(x_ref.min(),x_ref.max(),500).reshape(-1,1)

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_nbsf, out_grad_times, label='Q-Chem 5.4.2-dev', s=3)
    out_times.plot(x_outseq, model_out.predict(x_outseq))
    ref_times.scatter(ref_nbsf, ref_grad_times, label='Q-Chem 5.4.1', s=3)
    ref_times.plot(x_refseq, model_ref.predict(x_refseq))
    plt.xlabel("number of basis functions")
    plt.ylabel("Time per gradient calculation [CPUs]")
    plt.legend()
    fig.savefig("grad_times_nbsf.pdf")
    plt.close(fig)


