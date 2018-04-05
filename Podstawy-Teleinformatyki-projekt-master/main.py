import cv2
import _tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog as fd

def faceRecog(imagePath):
    cascPath = "haarcascade_frontalface_default.xml"

    faceCascade = cv2.CascadeClassifier(cascPath)

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #cv2.imshow("Faces found" ,image)

    cv2.imwrite("recognize.png", image)
    #cv2.waitKey(0)

    return image


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # create window
        # load initial image
        self.filename = fd.askopenfilename(filetypes=[("Obraz", "*.png")])  # wywolanie okna dialogowego open file
        if self.filename:

            self.img = ImageTk.PhotoImage(Image.open(self.filename))
            # display it in a label
            self.label = tk.Label(self, image=self.img)
            self.label.pack(fill='both', expand=True)

            tk.Button(self, text="Update", command=self.update_image).pack()

            self.mainloop()

    def update_image(self):
        # code to capture new image here
        # ...
        # load new image
        image1 = faceRecog(self.filename)

        self.img = ImageTk.PhotoImage(Image.open("recognize.png"))
        # update label image
        self.label.configure(image=self.img)

if __name__ == '__main__':
    App()