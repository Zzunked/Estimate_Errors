import sys
from PyQt5 import QtWidgets
from estimate_errors.main_gui import MainGUI

def main_exec():
    app = QtWidgets.QApplication(sys.argv)
    win = MainGUI()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main_exec()