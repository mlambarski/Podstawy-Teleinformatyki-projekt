#!/usr/bin/env python

import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import socket
from threading import Thread
import csv
import tkinter.scrolledtext as tkscrolled

width, height = 450, 450
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

received_data = ''

root = tk.Tk()
lmain = tk.Label(root)
lmain.pack()
textarea = tkscrolled.ScrolledText(root, height=15, width=40)
textarea.pack(side=LEFT)
read_csv = Text(root, height=2, width=30)
read_csv.pack(side=TOP)
save_csv = Text(root, height=2, width=30)
save_csv.pack(side=BOTTOM)


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


def show_button_read():
    read_button = Button(root, height=2, width=30, text="Wczytaj liste", fg="black", command=callback_read)
    read_button.pack(side=TOP)


def show_button_write():
    save_button = Button(root, height=2, width=30, text="Zapisz liste", fg="black", command=callback_write)
    save_button.pack(side=BOTTOM)


def callback_read():
    input_csv = read_csv.get("1.0", "end-1c")
    textarea.delete('1.0', END)

    if (input_csv != ''):
        with open(input_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader:
                textarea.insert('end', row[0] + " ")
                textarea.insert('end', row[1] + " ")
                textarea.insert('end', row[2])
                textarea.insert('end', "\n")


def connection():
    TCP_IP = ''
    TCP_PORT = 5005
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)

    while 1:
        data = conn.recv(BUFFER_SIZE)

        s.listen(1)
        if (data.decode("utf-8") != ''):
            print("received data:" + data.decode("utf-8"))
            received_data = data.decode("utf-8")
            data = received_data.split(" ")
            string = textarea.get('1.0', END + '-1c').splitlines()
            textarea.delete('1.0', END)
            for x in string:
                row = x.split(" ")
                if ((row[0] == data[0]) and (row[1] == data[1])):
                    row[2] = 1
                textarea.insert('end', str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
                textarea.insert('end', "\n")






def callback_write():
    try:
        output_csv = save_csv.get("1.0", "end-1c")
        string = textarea.get('1.0', END + '-1c').splitlines()
        if (output_csv != ''):
            with open(output_csv, 'w', newline='') as new_csvfile:
                for x in string:
                    row = x.split(" ")
                    wr = csv.writer(new_csvfile, quoting = csv.QUOTE_ALL)
                    # print(str(row[0])+ "," +str(row[1])+ "," +str(row[2]))
                    wr.writerow([row[0], row[1], row[2]])

    finally:
        pass



if __name__ == "__main__":
    thread = Thread(target=connection, args=())
    thread.start()
    show_hog()
    show_button_read()
    show_button_write()
    root.mainloop()

