import sys

import usb
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from ui.main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_list_usb.setText('List USB')
        self.ui.btn_list_usb.clicked.connect(self.list_usb)
        self.ui.btn_find_usb.setText('Find USB')
        self.ui.btn_find_usb.clicked.connect(self.find_specific_device)

    def list_usb(self):
        try:
            dev = usb.core.find(find_all=True)
            list_usb = list(dev)
            for cfg in list_usb:
                cfg.set_configuration()
                print('VendorID={}(0x{:04X}) & ProductID={}(0x{:04X})'.format(str(cfg.idVendor), cfg.idVendor,
                                                                              str(cfg.idProduct), cfg.idProduct))
                print('-------------------------------------------------------------------------------------')
        except Exception as e:
            print(e)

    def find_specific_device(self):
        # find our device
        dev = usb.core.find(idVendor=0x3231, idProduct=0x0100)

        # was it found?
        if dev is None:
            # raise ValueError('Device not found')
            QMessageBox.information(self, "Warning", "Device not found", QMessageBox.Close)

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]

        ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)

        assert ep is not None

        # write the data
        ep.write('test')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
