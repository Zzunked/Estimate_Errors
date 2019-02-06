import sys
from PyQt5 import QtWidgets
from estimate_errors.indirerror import IndirErrorGUI

def err_main_exec():
    app = QtWidgets.QApplication(sys.argv)
    win = IndirErrorGUI()
    win.show()
    app.exec_()

if __name__ == '__main__':
    err_main_exec()