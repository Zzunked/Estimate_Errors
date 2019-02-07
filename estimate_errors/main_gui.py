from PyQt5 import QtWidgets

from estimate_errors.direrrorGUI import Ui_MainWindow_DirError
from estimate_errors.indirerrorGUI import Ui_MainWindow_IndirError
from estimate_errors.main_functions import *


class DirErrorGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow_DirError()
        self.ui.setupUi(self)

        self.ui.inputValuesBtn.clicked.connect(self.inputValues)
        self.ui.appErrorBtn.clicked.connect(self.inputAppError)
        self.ui.measureErrorBtn.clicked.connect(self.inputMeasureError)
        self.ui.resultBtn.clicked.connect(self.showDirError)
        self.ui.listClearBtn.clicked.connect(self.ui.listWidget.clear)

        self.ui.actionSave.triggered.connect(self.saveResult)
        self.ui.actionOpen.triggered.connect(self.openTxtFile)
        self.ui.actionHelp.triggered.connect(self.helpinfo)

        self.ui.listWidget.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")


    def openTxtFile(self):
        global inp_values, inp_app_error, inp_measure_err
        try:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл", '', "(*.txt)")
            file = re.sub(' ', '', open(path).read()).split('\n')
            inp_values = file[0].split(':')[1]
            inp_app_error = file[1].split(':')[1]
            inp_measure_err = file[2].split(':')[1]

            self.ui.listWidget.addItem('Измеренные значения: ' + inp_values)
            self.ui.listWidget.addItem('Приборная погрешность: ' + inp_app_error)
            self.ui.listWidget.addItem('Погрешность измерения: ' + inp_measure_err)
        except:
            QtWidgets.QMessageBox.about(self,
                                        'Ошибка',
                                        'Вы неправильно составили txt файл!\n'
                                        'Пример правильного txt файла:\n'
                                        'x: 3.8,3.9,3.7,4,4.1,3.8 \n'
                                        'apperr: 0.05\n'
                                        'measerr: 0.1\n')

    def saveResult(self):
        try:
            if dir_err_result: pass
            fname, sel = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить","",
                                                               "Text Files (*.txt);;untitled.txt")
            if fname:
                with open(fname, 'w') as f:
                    f.write('average error\n')
                    f.write(str(dir_err_result[0]) + ' ' + str(dir_err_result[1]) + '\n')
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала вычислите погрешность!')

    def helpinfo(self):
        text = open('docs/dir_help_info.txt').read()
        self.ui.listWidget.addItem(text)

    def inputValues(self):
        global inp_values
        inp_values, ok = QtWidgets.QInputDialog.getText(self,
                                                       'Измеренные значения',
                                                       'Введите измеренные значения через запятую:')
        if ok and inp_values != '':
            text= 'Измеренные значения: ' + inp_values
            self.ui.listWidget.addItem(text)

    def inputAppError(self):
        global inp_app_error
        inp_app_error, ok = QtWidgets.QInputDialog.getText(self,
                                                           'Приборная погрешность',
                                                           'Введите приборную погрешность:')
        if ok and inp_app_error != '':
            text = 'Приборная погрешность: ' + inp_app_error
            self.ui.listWidget.addItem(text)

    def inputMeasureError(self):
        global inp_measure_err
        inp_measure_err, ok = QtWidgets.QInputDialog.getText(self,
                                                             'Погрешность измерения',
                                                             'Введите погрешность измерения:')
        if ok and inp_measure_err != '':
            text = 'Погрешность измерения: ' + inp_measure_err
            self.ui.listWidget.addItem(text)

    def showDirError(self):
        global dir_err_result
        try:
            if inp_values and inp_app_error and inp_measure_err: pass
            dir_err_result = est_dir_err(inp_values, inp_app_error, inp_measure_err)
            text = 'Среднее значение: ' \
                   + str(dir_err_result[0]) + ' Погрешность: ' \
                   + str(dir_err_result[1]) + ' Процент погрешности: ' \
                   + str(dir_err_result[2]) + '%'

            self.ui.listWidget.addItem(text)
            self.ui.listWidget.addItem(' ')
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала введите значения измеряемой величины, '
                                                        'приборную погрешность и '
                                                        'погрешность измерения!')

class MainGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow_IndirError()
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
            indir_err_vals = est_indir_err(inp_func, inp_vals, inp_errors, math_funcs)
            for x in range(len(indir_err_vals[0])):
                text = ('Значение функции: ' + str(indir_err_vals[0][x]) +
                            ' Погрешность: ' + str(indir_err_vals[1][x]) +
                            ' Процент погрешности: ' + str(indir_err_vals[2][x]) + '%')
                self.ui.listWidget.addItem(text)
        except NameError:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Сначала введите функцию и значения переменных!')

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
            plot_func_w_errors(indir_err_vals, 1, math_funcs, graph_title=graph_title, y_label=y_label, x_label=x_label)
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
                plot_func_w_errors(indir_err_vals, 2, math_funcs, graph_title=graph_title, y_label=y_label, x_label=x_label)
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
                                                                                  'Введите название графика')
                            y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                                              'Введите название оси ординат')
                            x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                                              'Введите название оси абсцисс')
                    except NameError:
                        graph_title, ok1 = QtWidgets.QInputDialog.getText(self, 'Название Графика',
                                                                              'Введите название графика')
                        y_label, ok2 = QtWidgets.QInputDialog.getText(self, 'Ось Oy',
                                                                          'Введите название оси ординат')
                        x_label, ok3 = QtWidgets.QInputDialog.getText(self, 'Ось Ox',
                                                                          'Введите название оси абсцисс')
                    plot_func_w_errors(indir_err_vals, 3, math_funcs,
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