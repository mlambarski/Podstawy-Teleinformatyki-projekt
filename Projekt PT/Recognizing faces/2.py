import cv2
import numpy as np 
import sqlite3
import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox



class Add_person(QDialog):
    
    def __init__(self):
        super(Add_person,self).__init__()
        loadUi('add_person.ui', self)      
        self.pushButton_doPhotos.clicked.connect(self.photos)

    def photos(self):
        self.conn = sqlite3.connect('database.db')
        if not os.path.exists('./dataset'):
            os.makedirs('./dataset')
        self.c = self.conn.cursor()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.uname = self.lineEdit_name.text()
        self.make()

   
    def make(self):
        if(self.uname != ''):
            print("Jestem w make")
            self.label_to_show.setText("")
            cap = cv2.VideoCapture(0)
            self.c.execute('INSERT INTO users (name) VALUES (?)', (self.uname, ))
            uid = self.c.lastrowid
            sampleNum = 0
            while True:
              ret, img = cap.read()
              gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              faces = self.face_cascade.detectMultiScale(gray, 1.3, 15)
              print(faces)
              for (x,y,w,h) in faces:
                sampleNum = sampleNum+1
                cv2.imwrite("dataset/User."+str(uid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                cv2.waitKey(100)
              cv2.imshow('img',img)
              cv2.waitKey(1);
              if sampleNum > 100:
                break
            cap.release()
            self.conn.commit()
            self.conn.close()
            cv2.destroyAllWindows()
        else:
            self.label_to_show.setText("Podaj imie i nazwisko osoby")
            self.label_to_show.setStyleSheet('color: red')
            


if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = Add_person()
    window.show()

    sys.exit(app.exec_())
