import sys
import cv2
import numpy as np 
import sqlite3
import os
import socket

from threading import Thread
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap, QImage 
from PyQt5.uic import loadUi
import cv2

TCP_IP = '192.168.43.119'
TCP_PORT = 5005
BUFFER_SIZE = 1024
        # MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


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
            self.c.execute("select name from users where id = (?);", (ids,))
            result = self.c.fetchall()
            name = result[0][0]

            if conf < 50:
                print("match")
                cv2.putText(self.image, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
                cv2.imwrite("test.png", self.image)
                with self.conn:
                    self.c=self.conn.cursor()
                    self.c.execute("UPDATE users SET status='rozpoznany' WHERE id = (?);", (ids,))
                    result = self.c.fetchall()
                    print("Rozpoznano osobe ")
                    thread = Thread(target = connection, args = (name,))
,3
                    thread.start()

            else:
                print("NO match")
                cv2.putText(self.image, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

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
    window = Life2Coding()
    window.setWindowTitle('Rozpoznawanie twarzy')
    window.show()
    sys.exit(app.exec_())