from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap, QImage 
from PyQt5.uic import loadUi
import cv2
import sys
from PyQt5.QtCore import pyqtSlot
import numpy as np 
import sqlite3
import os
import socket
from threading import Thread
from time import sleep
from PIL import Image

class Admin(QDialog):
    def __init__(self):
        super(Admin,self).__init__()
        loadUi('admin.ui', self)  
    
        self.pushButton_add.clicked.connect(self.addperson)
        self.pushButton_teach.clicked.connect(self.teach)
        self.pushButton_show.clicked.connect(self.recognize)

    @pyqtSlot()
    def addperson(self):
        window = Add_person()
        window.setWindowTitle('Dodanie osoby')
        window.show()
        window.exec_()     
  
    @pyqtSlot()
    def teach(self):
        window = Teach()
        window.teach()


    @pyqtSlot()
    def recognize(self):
        window = Life2Coding()
        window.setWindowTitle('Rozpoznawanie osob')
        window.show()
        window.exec_()

"""
TCP_IP = '192.168.43.119'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
"""
class Teach(QDialog):
    def __init__(self):
        super(Teach,self).__init__()

    def teach(self):
        recognizer = cv2.createLBPHFaceRecognizer()
        path = 'dataset'
        if not os.path.exists('./recognizer'):
            os.makedirs('./recognizer')
        def getImagesWithID(path):
          imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
          faces = []
          IDs = []
          for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("training",faceNp)
            cv2.waitKey(10)
          return np.array(IDs), faces
        Ids, faces = getImagesWithID(path)
        recognizer.train(faces,Ids)
        recognizer.save('recognizer/trainingData.yml')
        cv2.destroyAllWindows()


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
            if cap is None or not cap.isOpened():
                self.label_kamera_busy.setText("Zamknij rozpoznawanie aby dodac osobe")
                self.label_kamera_busy.setStyleSheet('color: red')
            else:
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
            

def connection(MESSAGE):
    print("POlaczenie")   
    s.send(MESSAGE)

class Life2Coding(QDialog):
    def __init__(self):
        super(Life2Coding,self).__init__()
        loadUi('lasttry.ui', self)      
        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)


    def start_webcam(self):

        self.capture = cv2.VideoCapture(0)
        if self.capture is None or not self.capture.isOpened():
            self.label_kamera_busy.setText("Zamknij dodawanie osoby aby rozpoznawac")
            self.label_kamera_busy.setStyleSheet('color: red')
        else:
            self.conn = sqlite3.connect('database.db')
            self.c = self.conn.cursor()
            fname = "recognizer/trainingData.yml"
            if not os.path.isfile(fname):
                print("Please train the data first")
                exit(0)
            self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            self.recognizer = cv2.createLBPHFaceRecognizer()
            self.recognizer.load(fname)

            self.timer=QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(5)     
        
    def update_frame(self):
        ret, self.image=self.capture.read()
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),3)
            ids,conf = self.recognizer.predict(gray[y:y+h,x:x+w])
            print(ids)
            self.c.execute("select name from users where id = (?);", (ids,))
            result = self.c.fetchall()
            print("Result: ", result)
            name = result[0][0]

            if conf < 50:
                print("match")
                cv2.putText(self.image, " ", (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
                cv2.imwrite("test.png", self.image)
                with self.conn:
                    self.c=self.conn.cursor()
                    self.c.execute("UPDATE users SET status='rozpoznany' WHERE id = (?);", (ids,))
                    result = self.c.fetchall()
                    print("Rozpoznano osobe ")
                    self.lineEdit_recognized.setText(name)
                    """thread = Thread(target = connection, args = (name,))
                    thread.start()"""

            else:
                print("NO match")
                cv2.putText(self.image, ' ', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

        self.image = cv2.flip(self.image,1)
        self.displayImage(self.image,1)

    def displayImage(self,img, window=1):
        qformat=QImage.Format_Indexed8
        if(len(img.shape)==3):
            if (img.shape[2]==4):
                qformat=QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage=QImage(img,img.shape[1], img.shape[0], img.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        if (window==1):
            self.label.setPixmap(QPixmap.fromImage(outImage))
            self.label.setScaledContents(True)
       
                
    def stop_webcam(self):
        self.timer.stop()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = Admin()
    window.setWindowTitle('Panel administratora')
    window.show()
    sys.exit(app.exec_())
