import sys

import firebase_admin
from firebase_admin import db
import json
import generate_base, new_lesson_form,teacher_form
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QButtonGroup, QListView, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import uic
from PyQt5.Qt import QImage
from PyQt5 import QtCore
import datetime

WEEKS = {"Пн":"Понедельник","Вт":"Вторник","Ср":"Среда","Чт":"Четверг","Пт":"Пятница","Суб":"Суббота"}

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('view/main.ui', self)
        
        hz = "BFrcCBMTPIywmGLZcRc51vRiVKc5O3OnCxZDawf4RKZk8xvHLS11RurIFhC-PANhWEP1FnUu2kLCbdbd0sP_fLg"
        db_url = "https://shudule-elikaevo-default-rtdb.asia-southeast1.firebasedatabase.app/"
        cred_obj = firebase_admin.credentials.Certificate('key.json')
        default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':db_url})
        
        self.klasses_view:QListView
        self.lessons_view:QListView
        
        self.weeks_btns:QButtonGroup
        
        self.table:QTableWidget
        
        self.add_klass:QPushButton
        self.add_lesson:QPushButton
        self.delete_lesson:QPushButton
        self.delete_klass:QPushButton
        self.update_btn:QPushButton
        self.edit_btn:QPushButton
        self.teacher_btn:QPushButton
        
        self.data_label:QLabel
        
        self.klasses_view.setStyleSheet("selection-background-color: lightblue")
        self.lessons_view.setStyleSheet("selection-background-color: lightblue")
        self.add_klass.setStyleSheet(" border-width: 2px; border-radius: 15px; border-color: rgb(0,255,0); border-style: outset; ")
        self.add_lesson.setStyleSheet(" border-width: 2px; border-radius: 15px; border-color: rgb(0,255,0); border-style: outset; ")
        self.delete_lesson.setStyleSheet(" border-width: 2px; border-radius: 15px; border-color: rgb(255, 0, 0); border-style: outset; ")
        self.delete_klass.setStyleSheet(" border-width: 2px; border-radius: 15px; border-color: rgb(255, 0, 0); border-style: outset; ")
        self.update_btn.setStyleSheet(" border-width: 3px; border-radius: 15px; border-color: rgb(153,153,0); border-style: outset; ")
        self.edit_btn.setStyleSheet(" border-width: 3px; border-radius: 15px; border-color: rgb(153,153,0); border-style: outset; ")
        self.teacher_btn.setStyleSheet(" border-width: 3px; border-radius: 15px; border-color: rgb(153,153,0); border-style: outset; ")
        
        data = datetime.date.today()
        if data.isoweekday() == 7:
            w = "Воскресенье"
        else:
            w = list(WEEKS.items())[data.isoweekday() - 1][1]
        self.data_label.setText(f"{data}\n{w}")
        self.update_list_klass()
        
        #tabel
        self.table.setColumnCount(2)
        
        #btns
        self.add_klass.clicked.connect(self.add_new_klass)
        self.update_btn.clicked.connect(self.update_list_klass)
        refresh_icon = QPixmap("img/refresh.png")
        delete_icon = QPixmap("img/delete.png")
        add_icon = QPixmap("img/add.png")
        self.update_btn.setIcon(QIcon(refresh_icon))
        self.add_klass.setIcon(QIcon(add_icon))
        self.add_lesson.setIcon(QIcon(add_icon))
        self.delete_lesson.setIcon(QIcon(delete_icon))
        self.delete_klass.setIcon(QIcon(delete_icon))
        
        self.add_lesson.clicked.connect(self.show_new_lesson_form)
        self.delete_lesson.clicked.connect(self.delete_lesson_func)
        self.delete_klass.clicked.connect(self.delete_klass_func)
        self.teacher_btn.clicked.connect(self.teacher_view)
        self.edit_btn.clicked.connect(self.edit_lesson)
        
    def select_klass_and_day(self):
        self.delete_klass.setEnabled(True)
        self.add_lesson.setEnabled(True)
        for index in self.klasses_view.selectedIndexes():
            item = self.klasses_view.model().itemData(index)
            t = self.weeks_btns.checkedButton().text()
            self.cur_date = self.all_shudule[item[0]][WEEKS[t]]
            self.item_list_2 = list(self.cur_date.keys()) 
            self.model_2 = QtCore.QStringListModel(self)
            self.model_2.setStringList(self.item_list_2)
            self.lessons_view.setModel(self.model_2)
            self.lessons_view.selectionModel().selectionChanged.connect(self.select_lesson)
            
    def update_teacher(self):
        ref = db.reference(f"/teachers/")
        data = list(ref.get().items())
        for num,t in enumerate(data):
            data[num] = f"{t[0]} {t[1]}"
        self.teacher_list = data 
        self.model_teacher = QtCore.QStringListModel(self)
        self.model_teacher.setStringList(self.teacher_list)
        self.teachers.teacher_view.setModel(self.model_teacher)
        
    def select_lesson(self):
        self.delete_lesson.setEnabled(True)
        self.edit_btn.setEnabled(True)
        self.table.clear()
        self.table.setRowCount(0)
        for index in self.lessons_view.selectedIndexes():
            item = self.lessons_view.model().itemData(index)
            try:
                for key,value in self.cur_date[item[0]].items():
                    rowPosition = self.table.rowCount()
                    self.table.insertRow(rowPosition)
                    self.table.setItem(rowPosition , 0, QTableWidgetItem(key))
                    self.table.setItem(rowPosition , 1, QTableWidgetItem(value))
            except AttributeError:
                rowPosition = self.table.rowCount()
                self.table.insertRow(rowPosition)
                self.table.setItem(rowPosition , 0, QTableWidgetItem("Уроков"))
                self.table.setItem(rowPosition , 1, QTableWidgetItem("нет"))
        
    def update_list_klass(self):
        ref = db.reference(f"/shudule/")
        self.all_shudule = ref.get()
        
        self.item_list = list(self.all_shudule.keys()) 
        self.model_1 = QtCore.QStringListModel(self)
        self.model_1.setStringList(self.item_list)
        self.klasses_view.setModel(self.model_1)
        
        #views
        self.klasses_view.selectionModel().selectionChanged.connect(self.select_klass_and_day)
        self.weeks_btns.buttonClicked.connect(self.select_klass_and_day)
        
    def show_new_lesson_form(self):
        klass_name = self.klasses_view.model().itemData(self.klasses_view.selectedIndexes()[0])[0]
        day_week = self.weeks_btns.checkedButton().text()
        ref = db.reference(f"/teachers/")
        teachers = list(ref.get().values())
        self.add_lesson_form = new_lesson_form.Lesson_Form(klass_name,day_week, self,teachers)
        self.add_lesson_form.show()
    
    def add_new_klass(self):
        text, ok_pressed = QInputDialog.getText(
            self, "Введите", "Название класса")
        if ok_pressed:
            new = generate_base.add_new_klass(text.upper())
            db.reference("/shudule/" + text.upper()).set(new)
            self.update_list_klass()
    
    def add_new_lesson(self, lesson, name_klass, week_day):
        new = list(lesson.items())[0]
        generate_base.new_lesson(new, name_klass, WEEKS[week_day])
        self.update_list_klass()
        
    def edit_lesson(self):
        klass_name = self.klasses_view.model().itemData(self.klasses_view.selectedIndexes()[0])[0]
        lesson = self.lessons_view.model().itemData(self.lessons_view.selectedIndexes()[0])[0]
        day_week = self.weeks_btns.checkedButton().text()
        ref = db.reference(f"/teachers/")
        teachers = list(ref.get().values())
        ref = db.reference(f"/shudule/{klass_name}/{WEEKS[day_week]}/{lesson}")
        data = ref.get()
        self.add_lesson_form = new_lesson_form.Lesson_Form(klass_name,day_week, self,teachers)
        self.add_lesson_form.line_cabinet.setText(data["кабинет"])
        self.add_lesson_form.line_item.setText(data["предмет"])
        self.add_lesson_form.combo_num_lesson.setCurrentText(lesson)
        self.add_lesson_form.combo_teacher.setCurrentText(data["учитель"])
        self.add_lesson_form.show()
        

    def delete_lesson_func(self):
        lesson = self.lessons_view.model().itemData(self.lessons_view.currentIndex())[0]
        klass = self.klasses_view.model().itemData(self.klasses_view.currentIndex())[0]
        week = self.weeks_btns.checkedButton().text()
        ref = db.reference(f"/shudule/{klass}/{WEEKS[week]}")
        if len(ref.get().keys()) == 1:
            db.reference(f"/shudule/{klass}/{WEEKS[week]}").set({"нет уроков":"нет уроков"})
        else:
            db.reference(f"/shudule/{klass}/{WEEKS[week]}/{lesson}").delete()
        self.update_list_klass()
        
    def delete_klass_func(self):
        db.reference(f"/shudule/{self.klasses_view.model().itemData(self.klasses_view.currentIndex())[0]}").delete()
        self.update_list_klass()
        
    def teacher_view(self):
        self.teachers = teacher_form.Teacher_Form(self)
        self.update_teacher()
        self.teachers.show()
    
    def add_teacher(self,fio):
        db.reference(f"/teachers/{fio[0]}").set(fio[1])
        
    def delete_teacher(self,last_name):
        db.reference(f"/teachers/{last_name}").delete()
        self.update_teacher()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    a = dict()
    sys.exit(app.exec())