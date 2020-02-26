import sys
import usb.core

from PyQt5 import QtWidgets, QtGui, QtCore

from ui.main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.setText('List USB')
        self.ui.pushButton.clicked.connect(self.list_usb)

    def list_usb(self):
        dev = usb.core.find(find_all=True)
        for cfg in dev:
            print('VendorID={}(0x{:04X}) & ProductID={}(0x{:04X})'.format(str(cfg.idVendor), cfg.idVendor,
                                                                  str(cfg.idProduct), cfg.idProduct))
            print('-------------------------------------------------------------------------------------')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
