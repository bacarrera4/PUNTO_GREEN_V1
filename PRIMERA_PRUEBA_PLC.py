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
        self.value = False
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
        self.button_cf.clicked.connect(self.read_coils)
        self. show()
    def troggle_on(self):
        client.write_coil(address=0, value=True)
        QTimer.singleShot(50, lambda: client.write_coil(0, False))
    def read_coils(self):
        self.response = client.read_coils(address=2, count=1)
        self.value = self.response.bits[0]
        # --- Detect FALLING EDGE (ON → OFF) ---
        if self.value:
            print("Process is done!")
        print("M2 =", self.value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Instantiate the custom window class
    main_window = Switch()
    sys.exit(app.exec())