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

class Lesson_Form(QMainWindow):

    def __init__(self, name_klass, day_week, main):
        super().__init__()
        uic.loadUi('view/new_lesson.ui', self)
        self.combo_end:QComboBox
        self.combo_start:QComboBox
        self.combo_klass:QComboBox
        self.combo_num_lesson:QComboBox
        self.combo_week:QComboBox
        
        self.line_cabinet:QLineEdit
        self.line_item:QLineEdit
        self.line_teacher:QLineEdit
        
        self.ok_btn:QPushButton
        self.cancel_btn:QPushButton
        
        
        #setup
        self.main = main
        self.combo_end.addItems(END_TIMES)
        self.combo_start.addItems(START_TIMES)
        self.combo_num_lesson.addItems(NUMS_LESSON)
        
        self.combo_klass.addItem(name_klass)
        self.combo_week.addItem(day_week)
        
        self.combo_num_lesson.currentTextChanged.connect(self.switch_num_lesson)
        self.ok_btn.clicked.connect(self.ok_btn_func)
    
    def switch_num_lesson(self, value):
        i = self.combo_num_lesson.currentIndex()
        self.combo_end.setCurrentIndex(i)
        self.combo_start.setCurrentIndex(i)
        
    def ok_btn_func(self):
        
        name_klass = self.combo_klass.currentText()
        num_lesson = self.combo_num_lesson.currentText()
        week_day = self.combo_week.currentText()
        
        lesson = self.line_item.text()
        num_cabinet = self.line_cabinet.text()
        teacher = self.line_teacher.text()
        
        start_time = self.combo_start.currentText()
        end_time = self.combo_end.currentText()
        
        new_lesson = {num_lesson:{
                    "класс": name_klass,
                    "учитель": teacher,
                    "предмет": lesson,
                    "кабинет": num_cabinet,
                    "начало":start_time,
                    "конец":end_time
                    }}
        self.main.add_new_lesson(new_lesson,name_klass,week_day)
        self.close()
        self.destroy()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lesson_Form("7А","Понедельник")
    ex.show()
    a = dict()
    sys.exit(app.exec())