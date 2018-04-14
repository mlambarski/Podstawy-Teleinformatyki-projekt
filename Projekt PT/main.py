import cv22 as cv2
import tkinter as tk
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
        self.window = tk.Tk.__init__(self,  className='Rozpoznawanie twarzy') # create window

        wybierz = tk.Button( self.window, text = "Wybierz plik", width=20, command=self.wybierz)
        photo = tk.Button( self.window, text = "Zrób zdjęcie", width=20, command=self.zdjecie)

        wybierz.pack()
        photo.pack()

        self.mainloop()

    def update_image(self):
        self.img = faceRecog(self.filename)

        self.img = ImageTk.PhotoImage(Image.open("recognize.png"))
        self.label.configure(image=self.img)

    def zdjecie(self):
        cap = cv2.VideoCapture(0)

        # Capture frame-by-frame
        ret, frame = cap.read()
        # do what you want with frame
        #  and then save to file
        cv2.imwrite('image.png', frame)


        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()



    def wybierz(self):
        self.filename = fd.askopenfilename(filetypes=[("Obraz", "*.png")])  # wywołanie okna dialogowego open file

        self.img = ImageTk.PhotoImage(Image.open(self.filename))
        # display it in a label
        self.label = tk.Label(self, image=self.img)
        self.label.pack(fill='both', expand=True)

        tk.Button(self, text="Wykryj twarze", command=self.update_image).pack()




if __name__ == '__main__':
    App()