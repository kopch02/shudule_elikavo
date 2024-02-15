import json
import firebase_admin
from firebase_admin import db

klass = "1А"
day_week = "понедельник"
num_lesson = "1"
teacher = "Марат Ринатович"
lesson =  "Информатика"
num_cabinet = "208"

start_time = "9:00"
end_time = "9:45"

WEEKS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"]

a = {klass:{
    day_week:{
        num_lesson:{
            "класс": klass,
            "учитель": teacher,
            "предмет": lesson,
            "кабинет": num_cabinet,
            "начало":start_time,
            "конец":end_time
            }
    }
}
}

def add_new_klass(name_klass):
    new = {day_week:{"нет уроков":"нет уроков"} for day_week in WEEKS}
    return new


def new_lesson(new:list|tuple,name_klass:str,week_day:str):
    ref = db.reference(f"/shudule/{name_klass}/{week_day}/")
    shudule = ref.get()
    try:
        if list(shudule.values())[0] == "нет уроков":
            new_lesson = {new[0]:new[1]}
            db.reference(f"/shudule/{name_klass}/{week_day}").set(new_lesson)
        else:
            db.reference(f"/shudule/{name_klass}/{week_day}/{new[0]}").set(new[1])

    except AttributeError:
        db.reference(f"/shudule/{name_klass}/{week_day}/{new[0]}").set(new[1])


if __name__ == "__main__":  
    add_new_klass("2А")