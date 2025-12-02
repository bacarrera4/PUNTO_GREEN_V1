import sys
from pymodbus.client import ModbusSerialClient
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt, QTimer
client = ModbusSerialClient(
    port="COM7",
    baudrate=19200,
    bytesize=8,
    parity='E',
    stopbits=1,
    timeout=0.5
)
class Switch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRUEBA PLC")
        self.setGeometry(0, 0, 720, 800)
        QTimer.singleShot(200, self.check_plc_connection)
        self.previous_value = False
        self.m2 = False
        self.thanks_window=None
        self.connected = False
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
        # Start TD0 monitor timer (every 200 ms)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.read_register)
        self.timer1.start(100)
        # label timer
        self.tittletd0 = QLabel(self)
        self.tittletd0.setGeometry(260, 400, 200, 30)
        self.tittletd0.setStyleSheet("color: green; font-size: 24pt;border: "
                                     "1px solid rgb(135, 206, 235);border-radius: 25px;")
        self.tittletd0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(110, 600, 500, 40)  # visible area
        self.progress.setRange(0, 50)
        self.progress.setValue(0)
        #self.progress.setStyleSheet("""QProgressBar {border: 2px solid #fbff1e;border-radius: 10px;text-align: center;background: #f7cc94;height: 25px;}QProgressBar::chunk {background-color: #ff5e1e;width: 20px;margin: 1px;}""")
        self.progress.setStyleSheet("""QProgressBar {border: 2px solid #ff8800;border-radius: 8px;background: #fff5e6;text-align: center;color: #cc6600;font-weight: bold;}QProgressBar::chunk {background-color: #ff6600;width: 15px;margin: 1px;}""")
        #self.progress.setStyleSheet("""QProgressBar {border: 2px solid #3fbf3f;border-radius: 10px;text-align: center;background: #d6ffd6;height: 25px;font-weight: bold;color: #006600;}QProgressBar::chunk {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #00ff00,stop:1 #009900);border-radius: 8px;}""")
        #self.progress.setStyleSheet("""QProgressBar {border: 2px solid #555;border-radius: 10px;text-align: center;background: #222;color: white;}QProgressBar::chunk {background-color: #00bfff;width: 20px;}""")
        self. show()
    def troggle_on(self):
        client.write_coil(0, True)  # Set M0 = 1
        QTimer.singleShot(50, lambda: client.write_coil(0, False))  # Reset M0
        print("START signal sent to PLC")
    def read_coils(self):
        if not self.connected:
            return  # Skip reading when PLC is offline
        rr = client.read_coils(24576, count=1)
        if rr.isError():
            return
        m2 = rr.bits[0]
        if self.previous_value and not m2:
            self.open_thanks()
        self.previous_value = m2
    def read_register(self):
        if not self.connected:
            return  # Prevent blocking
        result = client.read_holding_registers(32768, count=1)
        if result.isError():
            return
        td0_value = result.registers[0]
        self.tittletd0.setText(str(td0_value) if td0_value != 0 else "")
        self.progress.setValue(td0_value)
    def open_thanks(self):
        if self.thanks_window is None:
            self.thanks_window = Thanks_Window()
        self.thanks_window.show()
        self.close()
    def check_plc_connection(self):
        self.connected = client.connect()
        if not self.connected:
            QMessageBox.critical(
                self,
                "PLC Error",
                "No se pudo conectar al PLC.\nVerifique el cable, puerto o alimentación."
            )
class Thanks_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GRACIAS")
        self.setGeometry(0, 0, 720, 800)
        # label name
        self.tittleth = QLabel(self)
        self.tittleth.setGeometry(260, 400, 200, 30)
        self.tittleth.setText("GRACIAS")
        self.tittleth.setStyleSheet("color: green; font-size: 24pt;border: "
                                     "1px solid rgb(135, 206, 235);border-radius: 25px;")
        self.tittleth.setAlignment(Qt.AlignmentFlag.AlignCenter)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Instantiate the custom window class
    main_window = Switch()
    sys.exit(app.exec())