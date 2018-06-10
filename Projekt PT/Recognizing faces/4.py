import cv2
import numpy as np 
import sqlite3
import os
import socket



class sending_message:
    def __init__(self):
        self.TCP_IP = "192.168.43.75"
        self.TCP_PORT = 50001

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.TCP_IP,self.TCP_PORT))

    def sendto(self, message):
        self.sock.send(message)
        data = self.sock.recv(1024)

    def close(self):
        self.sock.close()


class face_recog:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        fname = "recognizer/trainingData.yml"
        if not os.path.isfile(fname):
            print("Please train the data first")
            exit(0)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.recognizer = cv2.createLBPHFaceRecognizer()
        self.recognizer.load(fname)

    def main_loop(self):
        while True:
              print(cv2.__version__)
              ret, img = self.cap.read()
              gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
              for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                ids,conf = self.recognizer.predict(gray[y:y+h,x:x+w])
                self.c.execute("select name from users where id = (?);", (ids,))
                result = self.c.fetchall()
                name = result[0][0]

                if conf < 50:
                  print("match")
                  cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
                  cv2.imwrite("test.png", img)
                  with self.conn:
                    self.c=self.conn.cursor()
                    self.c.execute("UPDATE users SET status='rozpoznany' WHERE id = (?);", (ids,))
                    result = self.c.fetchall()
                    print("Rozpoznano osobe ")
                    
                    """client = sending_message()
                    client.connect()
                    client.sendto(name)
                    client.close()"""
                else:
                  print("NO match")
                  cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

              cv2.imshow('Face Recognizer',img)
              k = cv2.waitKey(30) & 0xff
              if k == 27:
                break

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


f = face_recog()
f.main_loop()
