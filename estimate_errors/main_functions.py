import re

import numpy as np

import matplotlib.pyplot as plt
import sympy as sy
from scipy.optimize import curve_fit

from estimate_errors.utils import mathematic_funcs

math_funcs = mathematic_funcs()

def est_indir_err(inp_func, inp_vals, inp_errors, math_funcs):
    input_str = re.sub("[^A-Za-z0-9\,()*/+=\-]", '', inp_func)
    func, variables = re.sub(' ', '', input_str).split('=')[1], re.sub(' ', '', input_str).split('(')[1].split(')')[0]
    str_vars = re.sub(',', '', variables)

    input_vals, const_vals, var_vals = {}, {}, {}

    for x in list(inp_vals.keys()):
        if len(inp_vals[x]) > 1:
            var_vals[x] = inp_vals[x]
        else:
            const_vals[x] = float(eval(inp_vals[x][0], math_funcs))

    val_list = []
    for x in list(var_vals.keys()):
        for y in var_vals[x]:
            d = const_vals.copy()
            d[x] = eval(y, math_funcs)
            val_list.append(d)
    derivatives = [str(sy.diff(func, x)) for x in str_vars]
    func_values = [eval(func, math_funcs, x) for x in val_list]

    der_vals = []
    for x in range(len(derivatives)):
        l = [(eval(derivatives[x], math_funcs, i) * inp_errors[x]) ** 2 for i in val_list]
        der_vals.append(l)
    func_errors = [np.sqrt(np.sum(x)) for x in list(zip(*np.array(der_vals)))]

    var_vals_vector = [float(eval(x, math_funcs)) for x in list(var_vals.values())[0]]
    for x in str_vars:
        if x == list(var_vals.keys())[0][0]:
            vals_vector_err = inp_errors[str_vars.index(x)]
            break

    errors_round, func_values_round = [], []
    for i in list(zip(func_errors, func_values)):
        if int(str(i[0]).split('.')[0]) != 0:
            errors_round.append(np.round(i[0], 0))
            func_values_round.append(np.round(i[1], 0))
        else:
            for x in str(i[0]).split('.')[1]:
                if int(x) != 0 and int(x) != 1:
                    errors_round.append(np.round(i[0], str(i[0]).split('.')[1].index(x) + 1))
                    func_values_round.append(np.round(i[1], str(i[0]).split('.')[1].index(x) + 1))
                    break
                elif int(x) == 0:
                    continue
                else:
                    errors_round.append(np.round(i[0], list(str(i[0]).split('.')[1]).index(x) + 2))
                    func_values_round.append(np.round(i[1], list(str(i[0]).split('.')[1]).index(x) + 2))
                    break

    error_percent = [np.abs(np.round(x[1] * 100 / x[0])) for x in list(zip(func_values_round, errors_round))]

    return func_values_round, errors_round, error_percent, var_vals_vector, vals_vector_err, func, variables


def est_dir_err(input_values, input_app_error, input_measure_error):
    values = [float(i) for i in re.sub(' ', '', input_values).split(',')]
    apperror = float(input_app_error)
    measurerror = float(input_measure_error)
    average = np.average(values)
    scattervals = np.sqrt(np.sum([(average - i) ** 2 / len(values) for i in values]))
    error = np.sqrt(scattervals ** 2 + apperror ** 2 + measurerror ** 2)

    if int(str(error).split('.')[0]) != 0:
        error_round = np.round(error, 0)
        average_round = np.round(average, 0)
    else:
        for x in str(error).split('.')[1]:
            if int(x) != 0 and int(x) != 1:
                error_round = np.round(error, str(error).split('.')[1].index(x) + 1)
                average_round = np.round(average, str(error).split('.')[1].index(x) + 1)
                break
            elif int(x) == 0:
                continue
            else:
                error_round = np.round(error, list(str(error).split('.')[1]).index(x) + 2)
                average_round = np.round(average, list(str(error).split('.')[1]).index(x) + 2)
                break
    error_percent = np.round(error_round * 100 / average_round)
    return average_round, error_round, error_percent


def plot_func_w_errors(func_and_errors, choose_plot, math_funcs, poly_degree=1, graph_title='Graph of Function',
                       y_label='Function', x_label='x_axis'):
    x = np.array(func_and_errors[3])
    y = np.array(func_and_errors[0])
    yerr = func_and_errors[1]
    xerr = func_and_errors[4]

    if func_and_errors[3][-1] > 0:
        xstep = np.array(func_and_errors[3][-1] / len(x))
    else:
        xstep = np.array(np.abs(func_and_errors[3][0]) / len(x))

    dx = xstep * 10 ** -3
    xdata = np.round(np.arange(func_and_errors[3][0] - xstep, func_and_errors[3][-1] + xstep, dx), decimals=4)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if choose_plot == 1:
        ax1.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', label=y_label.split(',')[0], ecolor='red')
    elif choose_plot == 2:
        func = eval('lambda ' + func_and_errors[6] + ':' + func_and_errors[5], math_funcs)
        popt, pcov = curve_fit(func, x, y)
        ax1.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', label=y_label.split(',')[0], ecolor='red')
        ax1.plot(xdata, func(xdata, *popt), label='Curve fit')
    else:
        polyfit_coeff = np.polyfit(x, y, poly_degree)
        coeff_names = 'abcdefghi'
        coeff_labels = list(zip(coeff_names, polyfit_coeff))
        poly_label = f'Polyfit, deg={poly_degree}\n'
        for i in range(poly_degree + 1):
            poly_label += str(coeff_labels[i][0]) + ':' + str(coeff_labels[i][1]) + '\n'
        poly_fit = np.poly1d(polyfit_coeff)
        ax1.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', label=y_label.split(',')[0], ecolor='red')
        ax1.plot(xdata, poly_fit(xdata), label=poly_label)

    plt.rc('grid', linestyle="--", color='black')
    plt.title(graph_title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.legend(loc='best')
    plt.grid(True)

    plt.show()
