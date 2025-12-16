import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QMouseEvent, QIcon, QLinearGradient, QBrush, QPalette, QColor, QFontDatabase
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QMessageBox, \
    QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QGridLayout
from supabase import create_client, Client

url="https://qiaqowxqtruwjbckwqok.supabase.co"
key=("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJp"
     "c3MiOiJzdXBhYmFzZSIsInJlZiI6InFpYXFvd3hxdH"
     "J1d2piY2t3cW9rIiwicm9sZSI6ImFub24iLCJpYXQiO"
     "jE3NjI4NzYwMjAsImV4cCI6MjA3ODQ1MjAyMH0.GoWSO"
     "slkBiwK-rtSgcLu3qln4AarYJna1Qr64bHXQMY")
supabase: Client = create_client(url, key)
class PrincipalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CARATULA")
        self.setGeometry(0, 0, 720, 800)
        # INSERTAR EL BACKGROUND
        b_label = QLabel(self)
        b_label.setGeometry(0, 0, 720, 800)
        b_img = QPixmap("pic/background.png")
        b_label.setPixmap(b_img)
        b_label.setScaledContents(True)
        b_label.lower()
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        QFontDatabase.addApplicationFont("fonts/Montserrat-VariableFont_wght.ttf")
        self.costumer_data_window=None
        self.select_product_window=None
        self.show()
    def open_product(self):
        if self.select_product_window is None:
            self.select_product_window = SelectProductWindow()
        self.select_product_window.show()
        self.close()
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_product()
class SelectProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SELECCIONAR PRODUCTO")
        self.setGeometry(0, 0, 720, 800)
        self.layout = QGridLayout(self)
        button_continue = QPushButton("CONTINUAR", self)
        button_continue.setStyleSheet("color: black; font-size: 10pt;font-weight: bold ;"
                                      "background-color: green;border: None; border-radius: 30px;")
        button_continue.setFixedSize(200, 60)
        self.layout.addWidget(button_continue, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        button_continue.clicked.connect(self.open_fac_fin)
    def open_fac_fin(self):
        if self.contQ != 0:
            if self.fac_fin_window is None:
                self.fac_fin_window = Final_Datos()
            self.fac_fin_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "AVISO", "EL VALOR NO PUEDE SER 0")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Instantiate the custom window class
    main_window = PrincipalWindow()
    sys.exit(app.exec())