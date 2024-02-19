import sys

import json
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QButtonGroup, QListView, QTableWidget, QTableWidgetItem, QPushButton, QComboBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import uic
from PyQt5 import QtCore

NUMS_LESSON = [f"{i + 1} урок" for i in range(7)]

START_TIMES = ["9:00","9:55","11:00","12:05","13:05","13:55","14:45"]
END_TIMES = ["9:45","10:40","11:45","12:50","13:50","14:40","15:30"]

class Teacher_Form(QMainWindow):

    def __init__(self, main):
        super().__init__()
        uic.loadUi('view/teacher.ui', self)
        self.teacher_view:QListView
        self.fio_edit:QLineEdit
        self.add_btn:QPushButton
        self.delete_btn:QPushButton
        
        delete_icon = QPixmap("img/delete.png")
        self.delete_btn.setStyleSheet(" border-width: 2px; border-radius: 15px; border-color: rgb(255, 0, 0); border-style: outset; ")
        
        #setup
        self.main = main
        
        self.add_btn.clicked.connect(self.ok_btn_func)
        self.delete_btn.setIcon(QIcon(delete_icon))
        self.delete_btn.clicked.connect(self.delete_teacher)
    
    def delete_teacher(self):
        teacher = self.teacher_view.model().itemData(self.teacher_view.selectedIndexes()[0])[0]
        self.main.delete_teacher(teacher.split()[0])
        
    def ok_btn_func(self):
        fio = self.fio_edit.text().split()
        if len(fio) != 3:
            print("тут не фио")
        else:
            fio = [fio[0] , f"{fio[1]} {fio[2]}"]
            self.main.add_teacher(fio)
        self.main.update_teacher()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Teacher_Form("asd")
    ex.show()
    a = dict()
    sys.exit(app.exec())