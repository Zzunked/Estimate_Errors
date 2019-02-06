import sys
from PyQt5 import QtWidgets
from estimate_errors.direrrorGUI import Ui_MainWindow
import re
import numpy as np



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
                error_round = np.round(error, str(error).split('.')[1].index(x)+1)
                average_round = np.round(average, str(error).split('.')[1].index(x)+1)
                break
            elif int(x) == 0:
                continue
            else:
                error_round = np.round(error, list(str(error).split('.')[1]).index(x) + 2)
                average_round = np.round(average, list(str(error).split('.')[1]).index(x) + 2)
                break
    error_percent = np.round(error_round*100/average_round)
    return average_round, error_round, error_percent


class DirErrorGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
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


def dir_err_main_exec():
    app1 = QtWidgets.QApplication(sys.argv)
    win1 = DirErrorGUI()
    win1.show()
    app1.exec_()


if __name__ == '__main__':
    dir_err_main_exec()