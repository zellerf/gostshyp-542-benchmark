import sys
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import split_dataset


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

    # split into training and test sets
    out_ntess_train, out_ntess_test = split_dataset.split_dataset(out_ntess)
    ref_ntess_train, ref_ntess_test = split_dataset.split_dataset(ref_ntess)
    out_grad_train, out_grad_test = split_dataset.split_dataset(out_grad_times)
    ref_grad_train, ref_grad_test = split_dataset.split_dataset(ref_grad_times)

    # linear regression
    x_out, y_out = np.array(out_ntess_train), np.array(out_grad_train)
    x_out = x_out.reshape(-1, 1)
    x_ref, y_ref = np.array(ref_ntess_train), np.array(ref_grad_train)
    x_ref = x_ref.reshape(-1, 1)
    model_ref = LinearRegression()
    model_ref.fit(x_ref, y_ref)
    model_out = LinearRegression()
    model_out.fit(x_out, y_out)

    # rmse
    x_test = np.array(out_ntess_test)
    x_test = x_test.reshape(-1, 1)
    y_test = model_out.predict(x_test)
    out_rmse = np.sqrt(metrics.mean_squared_error(y_test, out_grad_test))
    x_test = np.array(ref_ntess_test)
    x_test = x_test.reshape(-1, 1)
    y_test = model_out.predict(x_test)
    ref_rmse = np.sqrt(metrics.mean_squared_error(y_test, ref_grad_test))

    # print regression metrics
    print("Performing linear regression of gradient timings to number of tesserae")
    print("old implementation y-intercept:", model_ref.intercept_)
    print("old implementation slope:", model_ref.coef_)
    print("old implementation R²:", model_ref.score(x_ref, y_ref))
    print("old implementation RMSE:", ref_rmse)
    print("new implementation y-intercept:", model_out.intercept_)
    print("new implementation slope:", model_out.coef_)
    print("new implementation R²:", model_out.score(x_out, y_out))
    print("new implementation RMSE:", out_rmse)

    # draw regression lines
    x_out = np.linspace(min(out_ntess), max(out_ntess), 500)
    y_out = model_out.predict(x_out.reshape(-1, 1))
    x_ref = np.linspace(min(ref_ntess), max(ref_ntess), 500)
    y_ref = model_ref.predict(x_ref.reshape(-1, 1))

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_ntess, out_grad_times, label='new implementation', s=3, color='#1B2ACC')
    out_times.plot(x_out, y_out, color='#1B2ACC')
    out_times.fill_between(x_out, y_out-out_rmse, y_out+out_rmse, alpha=0.25, edgecolor='#1B2ACC', facecolor='#089FFF')
    ref_times.scatter(ref_ntess, ref_grad_times, label='old implementation', s=3, color='#CC4F1B')
    ref_times.plot(x_ref, y_ref, color='#CC4F1B')
    ref_times.fill_between(x_ref, y_ref-ref_rmse, y_ref+ref_rmse, alpha=0.25, edgecolor='#CC4F1B', facecolor='#FF9848')
    plt.ylim(bottom=0)
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

    # split into training and test sets
    out_nbsf_train, out_nbsf_test = split_dataset.split_dataset(out_nbsf)
    ref_nbsf_train, ref_nbsf_test = split_dataset.split_dataset(ref_nbsf)

    # quadratic regression
    x_out, y_out = np.array(out_nbsf_train), np.array(out_grad_train)
    x_out = x_out.reshape(-1, 1)
    x_ref, y_ref = np.array(ref_nbsf_train), np.array(ref_grad_train)
    x_ref = x_ref.reshape(-1, 1)
    model_ref = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model_ref.fit(x_ref, y_ref)
    model_out = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model_out.fit(x_out, y_out)

    # rmse
    x_test = np.array(out_nbsf_test)
    x_test = x_test.reshape(-1, 1)
    y_test = model_out.predict(x_test)
    out_rmse = np.sqrt(metrics.mean_squared_error(y_test, out_grad_test))
    x_test = np.array(ref_nbsf_test)
    x_test = x_test.reshape(-1, 1)
    y_test = model_out.predict(x_test)
    ref_rmse = np.sqrt(metrics.mean_squared_error(y_test, ref_grad_test))

    print("Performing quadratic regression of gradient timings to number of basis functions")
    print("old implementation y-intercept:", model_ref.named_steps['linearregression'].intercept_)
    print("old implementation coeffs:", model_ref.named_steps['linearregression'].coef_)
    print("old implementation R²:", model_ref.score(x_ref, y_ref))
    print("old implementation RMSE:", ref_rmse)
    print("new implementation y-intercept:", model_out.named_steps['linearregression'].intercept_)
    print("new implementation coeffs:", model_out.named_steps['linearregression'].coef_)
    print("new implementation R²:", model_out.score(x_out, y_out))
    print("new implementation RMSE:", out_rmse)

    # draw regression lines
    x_out = np.linspace(min(out_nbsf), max(out_nbsf), 500)
    y_out = model_out.predict(x_out.reshape(-1, 1))
    x_ref = np.linspace(min(ref_nbsf), max(ref_nbsf), 500)
    y_ref = model_ref.predict(x_ref.reshape(-1, 1))

    # plot
    fig = plt.figure()
    out_times = plt.subplot()
    ref_times = plt.subplot()
    out_times.scatter(out_nbsf, out_grad_times, label='new implementation', s=3, color='#1B2ACC')
    out_times.plot(x_out, y_out, color='#1B2ACC')
    out_times.fill_between(x_out, y_out-out_rmse, y_out+out_rmse, alpha=0.25, edgecolor='#1B2ACC', facecolor='#089FFF')
    ref_times.scatter(ref_nbsf, ref_grad_times, label='old implementation', s=3, color='#CC4F1B')
    ref_times.plot(x_ref, y_ref, color='#CC4F1B')
    ref_times.fill_between(x_ref, y_ref-ref_rmse, y_ref+ref_rmse, alpha=0.25, edgecolor='#CC4F1B', facecolor='#FF9848')
    plt.ylim(bottom=0)
    plt.xlabel("number of basis functions")
    plt.ylabel("Time per gradient calculation [CPUs]")
    plt.legend()
    fig.savefig("grad_times_nbsf.pdf")
    plt.close(fig)


