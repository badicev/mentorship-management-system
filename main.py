from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow
from  PyQt6.QtGui import QAction
import sys

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

app = QApplication(sys.argv)
nana = MainWindow()
nana.show()
sys.exit(app.exec())
