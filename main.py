from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget
from  PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow): #QMainWindow allows us to add a menu bar and a tool bar and a status bar.
# #also we can add divisions. better for larger apps
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mentorluk Programı Takip Uygulaması")

        file_menu_item = self.menuBar().addMenu("&Dosya") # add & to specify that is a menu item
        help_menu_item = self.menuBar().addMenu("&Yardım")

        add_student_action = QAction("Öğrenci ekle", self) #to add sub-menu
        file_menu_item.addAction(add_student_action)

        about_action = QAction("Hakkında", self) #self will connect this QAction to the class
        help_menu_item.addAction(about_action)
        #about_action.setMenuRole(QAction.MenuRole.NoRole) #if help menu doesn't show up

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(("ID", "İsim", "Grup", "Mentor", "Mentee Telefon", "Mentee E-posta", "Mentor Telefon", "Mentor E-posta")) #tuple
        self.setCentralWidget(self.table)
    def load_data(self):
        connection = sqlite3.connect("mentorship.db")
        result = connection.execute("SELECT * ")
        self.table

app = QApplication(sys.argv)
nana = MainWindow()
nana.show()
sys.exit(app.exec())
