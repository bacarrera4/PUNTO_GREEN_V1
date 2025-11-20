import sys
from openpyxl import load_workbook, Workbook
from pathlib import Path
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QMouseEvent, QIcon, QLinearGradient, QBrush, QPalette, QColor, QFontDatabase
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsOpacityEffect,  QGraphicsDropShadowEffect
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
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.main_window = None
        self.costumer_data_window = None
        self.quantity_window = None
        self.fac_fin_window = None
        self.contQ=0
        w_w=720
        h_w=800
        # INSERTAR EL BOTON DE SALIDA
        button_exit = QPushButton(self)
        button_exit.setGeometry(650, 0, 50, 50)
        button_exit.setIcon(QIcon("pic/exit.png"))
        button_exit.setIconSize(QSize(50, 50))
        button_exit.clicked.connect(self.open_main)
        #Boton para continuar
        porx=50
        pory = 50
        bc_w=150
        bc_h=75
        xpos=int((w_w*(porx/100))-(bc_w/2))
        ypos = int((h_w * (pory / 100)) - (bc_h / 2))
        button_continue = QPushButton("CONTINUAR",self)
        button_continue.setGeometry(xpos, ypos, bc_w, bc_h)
        button_continue.setStyleSheet("color: black; font-size: 10pt;font-weight: bold ;"
                                      "background-color: green;border: None; border-radius: 30px;")
        button_continue.clicked.connect(self.open_fac_fin)
        # INSERTAR BOTON DE SUMA
        button_sum = QPushButton(self)
        button_sum.setGeometry(640, 160, 40, 40)
        button_sum.setIcon(QIcon("pic/plus.png"))
        button_sum.setIconSize(QSize(40, 40))
        button_sum.clicked.connect(self.q_product_sum)
        # INSERTAR BOTON DE RESTA
        button_res = QPushButton(self)
        button_res.setGeometry(600, 160, 40, 40)
        button_res.setIcon(QIcon("pic/minus.png"))
        button_res.setIconSize(QSize(40, 40))
        button_res.clicked.connect(self.q_product_res)
        # label cantidad producto
        self.tittleQ = QLabel(self)
        self.tittleQ.setGeometry(600, 200, 80, 80)
        self.tittleQ.setText(f"{self.contQ}")
        self.tittleQ.setStyleSheet("color: black; font-size: 10pt;font-weight: bold ;"
                                   "background-color: white;border: None;")
        self.tittleQ.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.show()
    def open_customer_data_window(self):
        if self.costumer_data_window is None:
            self.costumer_data_window = CostumerDataWindow()
        self.costumer_data_window.show()
        self.close()
    def open_main(self):
        if self.main_window is None:
            self.main_window = PrincipalWindow()
        self.main_window.show()
        self.close()
    def open_fac_fin(self):
        if self.contQ != 0:
            if self.fac_fin_window is None:
                self.fac_fin_window = Final_Datos()
            self.fac_fin_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "AVISO", "EL VALOR NO PUEDE SER 0")
    def q_product_sum(self):
        if self.contQ < 25:
            self.contQ += 1
            self.tittleQ.setText(f"{self.contQ}")
        else:
            QMessageBox.warning(self, "AVISO", "EL VALOR DEBE ESTAR ENTRE 0 Y 25 LITROS")
    def q_product_res(self):
        if 1 <= self.contQ:
            self.contQ -= 1
            self.tittleQ.setText(f"{self.contQ}")
        else:
            QMessageBox.warning(self, "AVISO", "EL VALOR DEBE ESTAR ENTRE 0 Y 25 LITROS")
class Final_Datos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FACTURA O CONSUMIDOR FINAL")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.main_window = None
        self.costumer_data_window = None
        self.final_product_window = None
        # label info frecuent client
        tittleinfofc = QLabel(self)
        tittleinfofc.setText("DESEA FACTURA CON DATOS O CONSUMIDOR FINAL")
        tittleinfofc.setGeometry(0, 50, 720, 800)
        tittleinfofc.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        tittleinfofc.setStyleSheet("color: green; font-size: 12pt;font-weight: bold ;")
        # INSERTAR EL BOTON DE SALIDA
        button_exit = QPushButton(self)
        button_exit.setGeometry(650, 0, 50, 50)
        button_exit.setIcon(QIcon("pic/exit.png"))
        button_exit.setIconSize(QSize(50, 50))
        button_exit.clicked.connect(self.open_main)
        # Boton para FACTURA CON DATOS
        button_cf = QPushButton("Factura con Datos", self)
        button_cf.setGeometry(250, 250, 220, 75)
        button_cf.setStyleSheet("color: black; font-size: 10pt;font-weight: bold ;"
                                "background-color: lightgreen;border: None; border-radius: 30px;")
        button_cf.clicked.connect(self.open_customer_data_window)
        # Boton para CONSUMIDOR FINAL
        button_cn = QPushButton("Consumidor Final", self)
        button_cn.setGeometry(250, 500, 220, 75)
        button_cn.setStyleSheet("color: black; font-size: 10pt;font-weight: bold ;"
                                "background-color: orange;border: None; border-radius: 30px;")
        button_cn.clicked.connect(self.open_customer_data_window)
        self.show()
    def open_customer_data_window(self):
        if self.costumer_data_window is None:
            self.costumer_data_window = CostumerDataWindow()
        self.costumer_data_window.show()
        self.close()
    def open_main(self):
        if self.main_window is None:
            self.main_window = PrincipalWindow()
        self.main_window.show()
        self.close()
    def open_final_product(self):
        if self.final_product_window is None:
            self.final_product_window = Final_Product()
        self.final_product_window.show()
        self.close()
class CostumerDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PUNTO GREEN DATA")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.main_window = None
        self.select_product_window=None
        self.ticket_window = None
        self.idr=0
        self.name_fr=''
        self.id_fr = ''
        self.email_fr=''
        self.add_fr=''
        w_w=720
        h_w=800
        #CONFIGURACION DE INPUT
        # Input box Ingreso de informacion
        #input name
        self.input_box_name = QLineEdit(self)
        self.input_box_name.setPlaceholderText("Type here...")
        self.input_box_name.setGeometry(250, 200, 200, 30)  # x, y, width, height}
        # input ID
        self.input_box_ID = QLineEdit(self)
        self.input_box_ID.setPlaceholderText("Type here...")
        self.input_box_ID.setGeometry(250, 300, 200, 30)  # x, y, width, height}
        # input email
        self.input_box_mail = QLineEdit(self)
        self.input_box_mail.setPlaceholderText("Type here...")
        self.input_box_mail.setGeometry(250, 400, 200, 30)  # x, y, width, height}
        # input address
        self.input_box_add = QLineEdit(self)
        self.input_box_add.setPlaceholderText("Type here...")
        self.input_box_add.setGeometry(250, 500, 200, 30)  # x, y, width, height}
        #INSERTAR BOTON
        button = QPushButton("REGISTRARSE", self)
        button.setGeometry(150, 650, 100, 70)
        button.clicked.connect(self.read_inputs)
        #BOTON PARA REGRESAR A PANTALLA FINAL
        button = QPushButton("INICIO", self)
        button.setGeometry(250, 650, 100, 70)
        button.clicked.connect(self.open_main)
        #INSERTAR LABEL DE TEXTO
        main_tittle=QLabel(self)
        main_tittle.setText("DATOS DE LA FACTURA")
        main_tittle.setGeometry(0, 50, 720,800 )
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        font = QFont()
        font.setFamily("Garamond")
        font.setBold(True)
        main_tittle.setStyleSheet("color: green; font-size: 24pt;")
        main_tittle.setFont(font)
        #INSERTAR EL LOGO
        logo_label = QLabel(self)
        logo_label.setGeometry(0,0,80,80)
        logo=QPixmap("pic/LOGO_FINAL.png")
        logo_label.setPixmap(logo)
        logo_label.setScaledContents(True)
        #INSERTAR LABELS DE INFORMACION
        #label name
        tittleN=QLabel(self)
        tittleN.setText("NOMBRE COMPLETO")
        tittleN.setGeometry(100, 200, 200, 30)
        tittleN.setFont(font)
        #label ID
        tittleID=QLabel(self)
        tittleID.setText("NÚMERO DE CÉDULA")
        tittleID.setGeometry(100, 300, 200, 30)
        tittleID.setFont(font)
        #label EMAIL
        tittleEM=QLabel(self)
        tittleEM.setText("E-MAIL")
        tittleEM.setGeometry(100, 400, 200, 30)
        tittleEM.setFont(font)
        #label ADDRESS
        tittleAD=QLabel(self)
        tittleAD.setText("DIRECCIÓN")
        tittleAD.setGeometry(100, 500, 200, 30)
        tittleAD.setFont(font)
        # INSERTAR BOTON
        button = QPushButton("finalizar", self)
        button.setStyleSheet("""
                            QPushButton { color: black;font-size: 11pt;font-weight: bold;
                                background-color: rgba(135, 206, 235, 200);  /* translucent orange */
                                border: 1px solid rgba(135, 206, 235, 80);
                                border-radius: 25px;
                            }
                            QPushButton:hover {background-color: rgba(255, 165, 0, 255);}
                            QPushButton:pressed {background-color: rgba(255, 140, 0, 255);}""")
        button.setGeometry(260, 500, 200, 70)
        self.show()
        # Funcion para leer los datos con el boton
    def read_inputs(self):
        try:
            self.text_name = self.input_box_name.text()  # <-- gets the text from the input box
            self.text_ID = self.input_box_ID.text()  # <-- gets the text from the input box
            self.text_mail = self.input_box_mail.text()
            self.text_add = self.input_box_add.text()
            # Validation
            if not self.text_name or not self.text_ID or not self.text_mail:
                QMessageBox.warning(self, "Error", "NOMBRE, CEDULA E E-MAIL SON NECESARIOS")
                return
            text_addr = str(self.text_add) if self.text_ID else None
            data = {"name": self.text_name, "id": self.text_ID, "email": self.text_mail, "address": text_addr}
            response = supabase.table("users").insert(data).execute()
            if response.data:
                QMessageBox.information(self, "Success", "User registered successfully!")
                self.input_box_name.clear()
                self.input_box_ID.clear()
                self.input_box_mail.clear()
                self.input_box_add.clear()
                self.open_ticket_window()
            else:
                QMessageBox.warning(self, "Error", f"Insert failed: {response}")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            print(e)
        #ABRIR LA PANTALLA PRINCIPAL
    def open_main(self):
        if self.main_window is None:
            self.main_window = PrincipalWindow()
        self.main_window.show()
        self.close()
    def open_product(self):
        if self.select_product_window is None:
            self.select_product_window = SelectProductWindow()
        self.select_product_window.show()
        self.close()
    def open_ticket_window(self):
        self.idr=1
        if self.ticket_window is None:
            self.ticket_window = TicketWindow(self.text_name, self.text_ID,self.text_mail,
                                                         self.text_add, self.name_fr, self.id_fr,
                                                         self.email_fr,self.add_fr,self.idr)
        self.ticket_window.show()
        self.close()
class TicketWindow(QWidget):
    def __init__(self, text_name, text_ID, text_mail, text_add, name_fr,id_fr,email_fr,add_fr, idr):
        super().__init__()
        self.setWindowTitle("PUNTO GREEN DELIVERY")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.main_window = None
        self.select_product_window=None        #BOTON PARA REGRESAR A PANTALLA FINAL
        button = QPushButton("INICIO", self)
        button.setGeometry(260, 650, 200, 70)
        button.setStyleSheet("""
                            QPushButton { color: black;font-size: 11pt;font-weight: bold;
                                background-color: rgba(135, 206, 235, 200);  /* translucent orange */
                                border: 1px solid rgba(135, 206, 235, 80);
                                border-radius: 25px;
                            }
                            QPushButton:hover {background-color: rgba(255, 165, 0, 255);}
                            QPushButton:pressed {background-color: rgba(255, 140, 0, 255);}""")
        button.clicked.connect(self.open_main)
        #INSERTAR LABEL DE TEXTO
        main_tittle=QLabel(self)
        main_tittle.setText("DATOS DE LA FACTURA")
        main_tittle.setGeometry(0, 50, 720,800 )
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        font = QFont()
        font.setFamily("Garamond")
        font.setBold(True)
        main_tittle.setStyleSheet("color: green; font-size: 24pt;")
        main_tittle.setFont(font)
        #INSERTAR EL LOGO
        logo_label = QLabel(self)
        logo_label.setGeometry(0,0,80,80)
        logo=QPixmap("LOGO_FINAL.png")
        logo_label.setPixmap(logo)
        logo_label.setScaledContents(True)
        #INSERTAR LABELS DE INFORMACION
        tittleN = QLabel(self)
        tittleID = QLabel(self)
        tittleEM = QLabel(self)
        tittleAD = QLabel(self)
        if idr==1:
            #label name
            tittleN.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>NOMBRE:</span> "
                f"<span style='color: black; font-size: 14pt;'>{text_name}</span>"
            )
            tittleN.setGeometry(110, 200, 500, 30)
            tittleN.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            #label ID
            tittleID.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>NÚMERO DE CÉDULA:</span> "
                f"<span style='color: black; font-size: 14pt;'>{text_ID}</span>"
            )
            tittleID.setGeometry(110, 300, 500, 30)
            tittleID.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            #label EMAIL
            tittleEM.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>E-MAIL:</span> "
                f"<span style='color: black; font-size: 14pt;'>{text_mail}</span>"
            )
            tittleEM.setGeometry(110, 400, 500, 30)
            tittleEM.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            #label ADDRESS
            tittleAD.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>DIRECCION:</span> "
                f"<span style='color: black; font-size: 14pt;'>{text_add}</span>"
            )
            tittleAD.setGeometry(110, 500, 500, 30)
            tittleAD.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            print(idr)
        else:
            # label name
            tittleN.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>NOMBRE:</span> "
                f"<span style='color: black; font-size: 14pt;'>{name_fr}</span>"
            )
            tittleN.setGeometry(110, 200, 500, 30)
            tittleN.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            # label ID
            tittleID.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>NÚMERO DE CÉDULA:</span> "
                f"<span style='color: black; font-size: 14pt;'>{id_fr}</span>"
            )
            tittleID.setGeometry(110, 300, 500, 30)
            tittleID.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            # label EMAIL
            tittleEM.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>E-MAIL:</span> "
                f"<span style='color: black; font-size: 14pt;'>{email_fr}</span>"
            )
            tittleEM.setGeometry(110, 400, 500, 30)
            tittleEM.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            # label ADDRESS
            tittleAD.setText(
                f"<span style='color: black; font-size: 14pt; font-weight: bold;'>DIRECCION:</span> "
                f"<span style='color: black; font-size: 14pt;'>{add_fr}</span>"
            )
            tittleAD.setGeometry(110, 500, 500, 30)
            tittleAD.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center horizontally
            print(idr)
        self.show()
        #ABRIR LA PANTALLA PRINCIPAL
    def open_main(self):
        if self.main_window is None:
            self.main_window = PrincipalWindow()
        self.main_window.show()
        self.close()
    def open_product(self):
        if self.select_product_window is None:
            self.select_product_window = SelectProductWindow()
        self.select_product_window.show()
        self.close()
class Payment_Method(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pantalla de despacho")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        # INSERTAR LABEL DE TEXTO
        main_tittle = QLabel(self)
        main_tittle.setText("METODO DE PAGO")
        main_tittle.setGeometry(0, 50, 720, 800)
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        self.show()
class Cash(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pantalla de despacho")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        # INSERTAR LABEL DE TEXTO
        main_tittle = QLabel(self)
        main_tittle.setText("METODO DE PAGO")
        main_tittle.setGeometry(0, 50, 720, 800)
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        self.show()
class Card(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pantalla de despacho")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        # INSERTAR LABEL DE TEXTO
        main_tittle = QLabel(self)
        main_tittle.setText("METODO DE PAGO")
        main_tittle.setGeometry(0, 50, 720, 800)
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        self.show()
class De_Una(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pantalla de despacho")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        # INSERTAR LABEL DE TEXTO
        main_tittle = QLabel(self)
        main_tittle.setText("METODO DE PAGO")
        main_tittle.setGeometry(0, 50, 720, 800)
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        self.show()
class Final_Product(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pantalla de despacho")
        self.setGeometry(0, 0, 720, 800)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.main_window = None
        self.select_product_window=None
        self.ticket_window = None
        self.idr=0
        self.text_name=''
        self.text_ID=''
        self.text_mail=''
        self.text_add=''
        #CONFIGURACION DE INPUT
        # Input box Ingreso de informacion
        # input ID
        self.input_box_fr_ID = QLineEdit(self)
        self.input_box_fr_ID.setPlaceholderText("Type here...")
        self.input_box_fr_ID.setGeometry(440, 300, 200, 30)  # x, y, width, height}
        #INSERTAR BOTON
        button = QPushButton("finalizar", self)
        button.setStyleSheet("""
                    QPushButton { color: black;font-size: 11pt;font-weight: bold;
                        background-color: rgba(135, 206, 235, 200);  /* translucent orange */
                        border: 1px solid rgba(135, 206, 235, 80);
                        border-radius: 25px;
                    }
                    QPushButton:hover {background-color: rgba(255, 165, 0, 255);}
                    QPushButton:pressed {background-color: rgba(255, 140, 0, 255);}""")
        button.setGeometry(260, 500, 200, 70)
        #INSERTAR LABEL DE TEXTO
        main_tittle=QLabel(self)
        main_tittle.setText("ENCONTREMOS AL CLIENTE")
        main_tittle.setGeometry(0, 50, 720,800 )
        main_tittle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_tittle.lower()
        font = QFont()
        font.setFamily("Garamond")
        font.setBold(True)
        main_tittle.setStyleSheet("color: green; font-size: 24pt;")
        main_tittle.setFont(font)
        #INSERTAR EL LOGO
        logo_label = QLabel(self)
        logo_label.setGeometry(0,0,80,80)
        logo=QPixmap("pic/LOGO_FINAL.png")
        logo_label.setPixmap(logo)
        logo_label.setScaledContents(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Instantiate the custom window class
    main_window = PrincipalWindow()
    sys.exit(app.exec())