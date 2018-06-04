#!/usr/bin/env python

import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import socket
from threading import Thread

width, height = 400, 400
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

root = tk.Tk()
lmain = tk.Label(root)
lmain.pack()

def connection():
    TCP_IP = ''
    TCP_PORT = 5005
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)

    while 1:
        data = conn.recv(BUFFER_SIZE)
        if (data.decode("utf-8") != ''):
            print("received data:" + data.decode("utf-8"))

thread = Thread(target=connection, args=())
thread.start()

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def show_hog():
    _, frame = cap.read()
    found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
    draw_detections(frame, found)
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_hog)

def show_list():
    textarea = Text(root, height=20, width=40)
    textarea.pack()

def callback():
    try:
        fp = open('lista.txt')
        lines = fp.readlines()


    finally:
        fp.close()

def show_buttons():
    read_button = Button(root, text="Wczytaj liste", fg="black", command=callback)
    read_button.pack(side=LEFT)
    save_button = Button(root, text="Zapisz liste", fg="black")
    save_button.pack(side=RIGHT)


show_hog()
show_list()
show_buttons()
root.mainloop()

# conn.close()