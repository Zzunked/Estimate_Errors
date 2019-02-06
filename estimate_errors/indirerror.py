import sys
from PyQt5 import QtWidgets
from estimate_errors.indirerrorGUI import Ui_MainWindow
import re
import numpy as np
import sympy as sy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from estimate_errors.direrror import DirErrorGUI


def est_indir_err(inp_func, inp_vals, inp_errors):
    math_funcs = {'sin': np.sin, 'arcsin': np.arcsin, 'sinh': np.sinh,
                  'cos': np.cos, 'cosh': np.cosh, 'arccos': np.arccos,
                  'tan': np.tan, 'arctan': np.arctan, 'tanh': np.tanh,
                  'log': np.log, 'sqrt': np.sqrt, 'exp': np.exp,
                  'pi': np.pi}

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


def plot_func_w_errors(func_and_errors, choose_plot, poly_degree=1, graph_title='Graph of Function',
                       y_label='Function', x_label='x_axis'):
    math_funcs = {'sin': np.sin, 'arcsin': np.arcsin, 'sinh': np.sinh,
                  'cos': np.cos, 'cosh': np.cosh, 'arccos': np.arccos,
                  'tan': np.tan, 'arctan': np.arctan, 'tanh': np.tanh,
                  'log': np.log, 'sqrt': np.sqrt, 'exp': np.exp,
                  'pi': np.pi}

    x = np.array(func_and_errors[3])
    y = np.array(func_and_errors[0])
    yerr = func_and_errors[1]
    xerr = func_and_errors[4]

    if func_and_errors[3][-1] > 0:
        xstep = np.array(func_and_errors[3][-1] / len(x))
    else:
        xstep = np.array(np.abs(func_and_errors[3][0]) / len(x))

    dx = xstep*10**-3
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


class IndirErrorGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.inpFuncBtn.clicked.connect(self.inputFunction)
        self.ui.inputVarsBtn.clicked.connect(self.inputVariables)
        self.ui.calcFuncBtn.clicked.connect(self.calcFunction)
        self.ui.plotFuncBtn.clicked.connect(self.plotFunction)
        self.ui.fitPlotBtn.clicked.connect(self.curveFitPlot)
        self.ui.polyFitBtn.clicked.connect(self.polyFit)
        self.ui.clearListBtn.clicked.connect(self.ui.listWidget.clear)

        self.ui.actionSave.triggered.connect(self.saveResult)
        self.ui.actionOpen.triggered.connect(self.openTxtFile)
        self.ui.actionHelp.triggered.connect(self.helpinfo)

        self.ui.dirErrorOpen.triggered.connect(self.dirErrorOpen)

        self.ui.listWidget.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")


    def inputFunction(self):
        global inp_func, inp_func_vars, str_func_vars
        try:
            inp_func, ok = QtWidgets.QInputDialog.getText(self,
                                                            'Функция',
                                                            'Введите функцию вида f(x1,x2,x3...)\n'
                                                            'Например: f(x,a,b,c)=a*x**2+b*x+c\n')
            if ok and inp_func != '':
                inp_func_vars = re.sub(' ', '', inp_func).split('(')[1].split(')')[0]
                str_func_vars = re.sub(',', '', inp_func_vars)
                text = 'Функция: ' + inp_func
                self.ui.listWidget.addItem(text)
        except:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Вы неправильно ввели функцию!')

    def inputVariables(self):
        global inp_vars, inp_vals, inp_errors
        try:
            inp_vals = {}
            inp_errors = []

            for x in str_func_vars:
                inp1, ok1 = QtWidgets.QInputDialog.getText(self, 'Введите значение',
                                                         f'Введите значения переменной {x} через запятую')
                inp2, ok2 =QtWidgets.QInputDialog.getText(self, 'Введите значение',
                                                         f'Введите значение погрешности {x}')

                if ok1 and ok2 and inp1 != '' and inp2 != '':
                    inp_vals[x] = re.sub(' ', '', inp1).split(',')
                    inp_errors.append(float(inp2))
                    text = f'{x}:' + inp1 + '\nПогрешность:' + f'{inp2}'
                    self.ui.listWidget.addItem(text)
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала введите функцию!')

    def calcFunction(self):
        global indir_err_vals
        try:
            try:
                indir_err_vals = est_indir_err(inp_func, inp_vals, inp_errors)
                for x in range(len(indir_err_vals[0])):
                    text = ('Значение функции: ' + str(indir_err_vals[0][x]) +
                            ' Погрешность: ' + str(indir_err_vals[1][x]) +
                            ' Процент погрешности: ' + str(indir_err_vals[2][x]) + '%')
                    self.ui.listWidget.addItem(text)
            except NameError:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала введите функцию и значения переменных!')
        except:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Что-то пошло не так!')

    def openTxtFile(self):
        global inp_func, inp_func_vars, str_func_vars, inp_vars, inp_vals, inp_errors
        try:
            path, _ =QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл", '', "(*.txt)")
            file = re.sub(' ', '', open(path).read()).split('\n')
            if file[-1] == '': file = file[:-1]

            inp_func = file[0]
            inp_func_vars = inp_func.split('(')[1].split(')')[0]
            str_func_vars = re.sub(',', '', inp_func_vars)
            self.ui.listWidget.addItem('Функция: ' + inp_func)

            inp_vals = {}
            inp_errors = []
            for x in file[1:]:
                var_name = x.split(':')[0]
                var_vals = x.split(':')[1].split(';')[0]
                var_err = x.split(':')[1].split(';')[1]
                inp_vals[var_name] = var_vals.split(',')
                inp_errors.append(float(var_err))
                text = f'{var_name}:' + var_vals + '\nПогрешность:' + f'{var_err}'
                self.ui.listWidget.addItem(text)
        except:
            QtWidgets.QMessageBox.about(self,
                                        'Ошибка',
                                        'Вы неправильно составили txt файл!\n'
                                        'Пример правильного txt файла:\n'
                                        'f(x,a,b,c)=a*x**2+b*x+c \n'
                                        'x:1,2,3,4,5,6,7,8,9,10; 0.5\n'
                                        'a:4; 0.1\nb:2; 0.5\nc:10; 1\n')

    def saveResult(self):
        try:
            if indir_err_vals: pass
            fname, sel = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить",
                                                               "", "Text Files (*.txt);;untitled.txt" )

            if fname:
                with open(fname, 'w') as f:
                    f.write('func error\n\n')
                    for x in range(len(indir_err_vals[0])):
                        f.write(str(indir_err_vals[0][x]) + ' ' + str(indir_err_vals[1][x]) + '\n')
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала рассчитайте значения функции!')

    def helpinfo(self):
        text = open('docs/indir_help_info.txt').read()
        self.ui.listWidget.addItem(text)



    def plotFunction(self):
        global graph_title, y_label, x_label
        try:
            if indir_err_vals: pass
            try:
                if graph_title == '' and y_label == '' and x_label == '':
                    graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                                      f'Введите название графика')
                    y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                                  f'Введите название оси ординат')
                    x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                                  f'Введите название оси абсцисс')
            except NameError:
                graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                           f'Введите название графика')
                y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                           f'Введите название оси ординат')
                x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                           f'Введите название оси абсцисс')
            plot_func_w_errors(indir_err_vals, 1, graph_title=graph_title, y_label=y_label, x_label=x_label)
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала рассчитайте значения функции!')

    def curveFitPlot(self):
        global graph_title, y_label, x_label
        try:
            try:
                if indir_err_vals: pass
                try:
                    if graph_title == '' and y_label == '' and x_label == '':
                        graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                                          f'Введите название графика')
                        y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                                      f'Введите название оси ординат')
                        x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                                      f'Введите название оси абсцисс')
                except NameError:
                    graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                               f'Введите название графика')
                    y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                               f'Введите название оси ординат')
                    x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                               f'Введите название оси абсцисс')
                plot_func_w_errors(indir_err_vals, 2, graph_title=graph_title, y_label=y_label, x_label=x_label)
            except NameError:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала рассчитайте значения функции!')
        except ValueError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Функция не имеет параметров!')

    def polyFit(self):
        global graph_title, y_label, x_label

        try:
            if indir_err_vals: pass
            inp_degree, ok = QtWidgets.QInputDialog.getText(self,
                                                            'Степень полинома',
                                                            'Введите сепень полинома (1-8)')
            try:
                if re.sub("[^0-9.]", '', inp_degree) != '' and\
                        int(np.round(float(re.sub("[^0-9.]", '', inp_degree)), 0)) < 9\
                        and int(np.round(float(re.sub("[^0-9.]", '', inp_degree)), 0)) > 0:
                    inp_degree_round = int(np.round(float(re.sub("[^0-9.]", '', inp_degree)), 0))
                    try:
                        if graph_title == '' and y_label == '' and x_label == '':
                            graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                                                  f'Введите название графика')
                            y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                                              f'Введите название оси ординат')
                            x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                                              f'Введите название оси абсцисс')
                    except NameError:
                        graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                                              f'Введите название графика')
                        y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                                          f'Введите название оси ординат')
                        x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                                          f'Введите название оси абсцисс')
                    plot_func_w_errors(indir_err_vals, 3,
                                           poly_degree=inp_degree_round,
                                           graph_title=graph_title, y_label=y_label, x_label=x_label)
                else:
                    QtWidgets.QMessageBox.about(self, 'Ошибка',
                                                'Вы не ввели степень полинома или ввели значение больше 8!')
            except NameError:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Вы не ввели степень полинома!')
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала рассчитайте значения функции!')

    def dirErrorOpen(self):
        self.dir_err = DirErrorGUI()
        self.dir_err.show()

    def clearAll(self):
        global graph_title, y_label, x_label
        graph_title, y_label, x_label = '', '', ''
        self.ui.listWidget.clear


def indir_err_main_exec():
    app = QtWidgets.QApplication(sys.argv)
    win = IndirErrorGUI()
    win.show()
    app.exec_()


if __name__ == '__main__':
    indir_err_main_exec()