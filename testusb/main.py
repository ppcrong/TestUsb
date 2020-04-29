import sys

import usb
import usb.backend.libusb1
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from ui.main_window import Ui_MainWindow

ENDPOINT_ADDRESS_MSG_IN = 0x01
ENDPOINT_ADDRESS_MSG_OUT = 0x02
ENDPOINT_ADDRESS_AUX_IN = 0x03
ENDPOINT_ADDRESS_AUX_OUT = 0x04


class MainWindow(QtWidgets.QMainWindow):
    global msg_in
    global msg_out
    global aux_in
    global aux_out

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
            print("%s libusb device(s) found..." % len(list_usb))
            for cfg in list_usb:
                print('-------------------------------------------------------------------------------------')
                print('VendorID={}(0x{:04X}) & ProductID={}(0x{:04X})'.format(str(cfg.idVendor), cfg.idVendor,
                                                                              str(cfg.idProduct), cfg.idProduct))
        except Exception as e:
            print(e)

    def find_specific_device(self):
        backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\Windows\System32\libusb0.dll")
        print("backend: %s" % backend)

        # find our device
        dev = usb.core.find(idVendor=0x3231, idProduct=0x0100, backend=backend)

        # was it found?
        if dev is None:
            # raise ValueError('Device not found')
            QMessageBox.information(self, "Warning", "USB Device not found", QMessageBox.Close)

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]

        # region [ENDPOINTS]
        msg_in = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_address(
            e.bEndpointAddress) == ENDPOINT_ADDRESS_MSG_IN)
        if msg_in is None:
            print('get USB ENDPOINT #1 msg_in fail !')
        else:
            print("\t[msg_in]\n%s" % msg_in)

        msg_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_address(
            e.bEndpointAddress) == ENDPOINT_ADDRESS_MSG_OUT)
        if msg_out is None:
            print('get USB ENDPOINT #2 msg_out fail !')
        else:
            print("\t[msg_out]\n%s" % msg_out)

        aux_in = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_address(
            e.bEndpointAddress) == ENDPOINT_ADDRESS_AUX_IN)
        if aux_in is None:
            print('get USB ENDPOINT #3 aux_in fail !')
        else:
            print("\t[aux_in]\n%s" % aux_in)

        aux_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_address(
            e.bEndpointAddress) == ENDPOINT_ADDRESS_AUX_OUT)
        if aux_out is None:
            print('get USB ENDPOINT #4 aux_out fail !')
        else:
            print("\t[aux_out]\n%s" % aux_out)
        # endregion [ENDPOINTS]


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
