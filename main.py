from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QComboBox, QToolBar

from  PyQt6.QtGui import QAction, QIcon, QPixmap
import sys
import sqlite3

class MainWindow(QMainWindow): #QMainWindow allows us to add a menu bar and a toolbar and a status bar.
# #also we can add divisions. better for larger apps
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mentorluk Programı Takip Uygulaması")

        file_menu_item = self.menuBar().addMenu("&Dosya") # add & to specify that is a menu item
        help_menu_item = self.menuBar().addMenu("&Yardım")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("images/add.png"), "Öğrenci ekle", self) #to add sub-menu
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("Hakkında", self) #self will connect this QAction to the class
        help_menu_item.addAction(about_action)
        #about_action.setMenuRole(QAction.MenuRole.NoRole) #if help menu doesn't show up

        search_action = QAction(QIcon("images/search.png"), "Öğrenci ara", self)  # to add sub-menu
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(("ID", "İsim", "Grup", "Mentor", "Mentee Telefon", "Mentee E-posta", "Mentor Telefon", "Mentor E-posta")) #tuple
        self.table.verticalHeader().setVisible(False) #to hide original index numbers
        self.setCentralWidget(self.table)
        self.setFixedSize(1000, 800) #To change the default window size


        # Create a QLabel widget for the header image
        header_label = QLabel(self)

        # Set the image path
        image_path = "images/logobandı.jpg"

        # Create a QPixmap object with the image
        pixmap = QPixmap(image_path)

        # Set the pixmap on the QLabel
        header_label.setPixmap(pixmap)

        # Set the size and position of the QLabel
        header_label.setGeometry(200, 600, 500, 100)

        # Set the aspect ratio policy to maintain the image's aspect ratio
        header_label.setScaledContents(True)



        #Create toolbar and toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)





    def load_data(self):
        connection = sqlite3.connect("mentorship.db")
        result = connection.execute("SELECT * FROM ogrenciler")
        self.table.setRowCount(0) #this is for that whenever we load the datai this data won't be added to existing data
        #nested for loop
        for row_number, row_data in enumerate(result): #row_number is 0, 1, 2 | row_data will be a tuple with the data
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Öğrenci Ekle")
        self.setFixedSize(500, 500)

        layout = QVBoxLayout()

        #add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Mentee İsim")
        layout.addWidget(self.student_name)

        #add combo box of group numbers
        self.group_number = QComboBox()
        available_group_numbers = ["Grup 1","Grup 2", "Grup 3"]
        self.group_number.addItems(available_group_numbers)
        layout.addWidget(self.group_number)

        # add mentor name widget
        self.mentor_name = QLineEdit()
        self.mentor_name.setPlaceholderText(" Mentor İsim")
        layout.addWidget(self.mentor_name)

        # add mentee number widget
        self.mentee_number = QLineEdit()
        self.mentee_number.setPlaceholderText("Mentee Numara")
        layout.addWidget(self.mentee_number)

        # add mentee e-mail widget
        self.mentee_email = QLineEdit()
        self.mentee_email.setPlaceholderText("Mentee E-posta")
        layout.addWidget(self.mentee_email)

        # add mentor number widget
        self.mentor_number = QLineEdit()
        self.mentor_number.setPlaceholderText("Mentor Numara")
        layout.addWidget(self.mentor_number)

        # add mentor e-mail widget
        self.mentor_email = QLineEdit()
        self.mentor_email.setPlaceholderText("Mentor E-posta")
        layout.addWidget(self.mentor_email)

        #Add a submit button
        button = QPushButton("Kaydet")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)



        self.setLayout(layout)
    def add_student(self):
        name = self.student_name.text()
        group = self.group_number.itemText(self.group_number.currentIndex())
        mentor = self.mentor_name.text()
        mentee_phone = self.mentee_number.text()
        mentee_email = self.mentee_email.text()
        mentor_phone = self.mentor_number.text()
        mentor_email = self.mentor_email.text()

        connection = sqlite3.connect("mentorship.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO ogrenciler (İsim, Grup, Mentor, [Mentee Telefon], [Mentee E-posta], [Mentor Telefon], [Mentor E-posta]) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, group, mentor, mentee_phone, mentee_email, mentor_phone, mentor_email))

        connection.commit()
        cursor.close()
        connection.close()
        management.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        #Set window title and size
        self.setWindowTitle("Mentee veya Mentor Bul")
        self.setFixedSize(300,300)

        #Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Mentee İsmi")
        layout.addWidget(self.student_name)

        #Create a button
        button = QPushButton("Bul")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

        def search(self):
            name = self.student_name.text()
            connection = sqlite3.connect("mentorship.db")
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM ogrenciler WHERE name = ?", (name,))
            rows = list(result)
            print(rows)
            items = management.table.findItems(name,Qt.MatchFlag.MatchFixedString)
            for item in items:
                print(item)
                management.table.item(item.row(), 1).setSelected(True)

            cursor.close()
            connection.close()

app = QApplication(sys.argv)
management = MainWindow()
management.show()
management.load_data()
sys.exit(app.exec())
