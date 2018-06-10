import sys
from PyQt4 import QtCore, QtGui, uic
import sqlite3
from PyQt4.QtGui import * 
from PyQt4.QtCore import *

qtCreatorFile = "main.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        c= sqlite3.connect("database.db")
        result = c.execute("select * from users")
        for data in result:
            print("Osoba: ", data[1])
            print("Status: ", data[2])
                    # set data
            self.tableWidget.setItem(0,0, QTableWidgetItem(data[1]))
            if(data[2]) is None:
                self.tableWidget.setItem(0,1, QTableWidgetItem(""))
            else:
                self.tableWidget.setItem(0,1, QTableWidgetItem(data[2]))
          
        
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    

