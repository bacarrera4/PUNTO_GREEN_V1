import sys
import time
from pymodbus import client
from pymodbus.client import ModbusSerialClient
from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QSlider, QPushButton
from PyQt6.QtCore import Qt, QTimer
client = ModbusSerialClient(
    port="COM7",           # <-- your RS-232 adapter port
    baudrate=19200,         # must match PLC settings
    bytesize=8,
    parity='E',
    stopbits=1,
    timeout=0.5
)
class Switch(QWidget):
    def __init__(self):
        super().__init__()
        self.previous_value = False
        self.m2 = False
        self.setWindowTitle("PRUEBA PLC")
        self.setGeometry(0, 0, 720, 800)
        self.button_cf = QPushButton("START",self)
        self.button_cf.setGeometry(250, 250, 220, 75)
        self.button_cf.setStyleSheet("""
            QPushButton {
                color: black;
                font-size: 10pt;
                font-weight: bold;
                background-color: lightgreen;
                border: none;
                border-radius: 30px;
            }

            QPushButton[pressed="true"] {
                background-color: #8fff8f;  /* slightly darker green */
            }
        """)
        self.button_cf.clicked.connect(self.troggle_on)
        # Start M2 monitor timer (every 200 ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_coils)
        self.timer.start(200)
        self. show()
    def troggle_on(self):
        client.write_coil(0, True)  # Set M0 = 1
        QTimer.singleShot(50, lambda: client.write_coil(0, False))  # Reset M0
        print("START signal sent to PLC")
    def read_coils(self):
        rr = client.read_coils(24576, count=1)
        if rr.isError():
            print("Modbus read error")
            return
        m2 = rr.bits[0]
        if self.previous_value and not m2:
            print("M2 turned OFF — Process finished!")
        self.previous_value = m2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Instantiate the custom window class
    main_window = Switch()
    sys.exit(app.exec())