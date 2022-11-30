from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QWidget, QTableView, QVBoxLayout, QFormLayout,QLineEdit, QDialogButtonBox, QGroupBox,QDialog,QComboBox ,QMessageBox, QListWidget
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QMouseEvent
import re
import sys

import pymongo
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np
import pandas as pd



def connect():
    try:
        client = pymongo.MongoClient("mongodb+srv://admin:<password>@cluster0.p3dimes.mongodb.net/?retryWrites=true&w=majority")
        database = client["Song"]
        conn = database["allsong"]
        return conn
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


        
class Create(QWidget):
    def __init__(self):
        super().__init__()
        layout =  QVBoxLayout()
        self.label = QLabel("Add New Data")
        self.formGroupBox = QGroupBox("Form")
        self.songLineEdit = QLineEdit()
        self.artistLineEdit = QLineEdit()
        self.writenByLineEdit = QLineEdit()
        self.soucreLineEdit = QLineEdit()
        self.timesLineEdit = QLineEdit()
        self.ratingLineEdit = QLineEdit()
        self.listenLineEdit = QLineEdit()
        self.createForm()
        
        
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        
        layout.addWidget(self.label)
        layout.addWidget(self.formGroupBox)
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def createForm(self):
  
        # creating a form layout
        formLayout = QFormLayout()
        formLayout.addRow(QLabel("Song:"),self.songLineEdit)
        formLayout.addRow(QLabel("Artist:"), self.artistLineEdit)
        formLayout.addRow(QLabel("Writen by:"), self.writenByLineEdit)
        formLayout.addRow(QLabel("Soucre:"), self.soucreLineEdit)
        formLayout.addRow(QLabel("Times:"), self.timesLineEdit)
        formLayout.addRow(QLabel("Rating:"), self.ratingLineEdit)
        formLayout.addRow(QLabel("Listen:"), self.listenLineEdit)
       
        # setting layout
        self.formGroupBox.setLayout(formLayout)
    def accept(self):
        print("Accepted")
        print(self.songLineEdit.text())
        print(self.artistLineEdit.text())
        print(self.writenByLineEdit.text())
        print(self.soucreLineEdit.text())
        print(self.timesLineEdit.text())
        print(self.ratingLineEdit.text())
        print(self.listenLineEdit.text())
        self.dialog()
        
        
        conn = connect()
        conn.insert_one({"Song":self.songLineEdit.text(),"Artist":self.artistLineEdit.text(),"Writen by":self.writenByLineEdit.text(),"Soucre":self.soucreLineEdit.text(),"Time":self.timesLineEdit.text(),"Rating":self.ratingLineEdit.text(),"Listen":self.listenLineEdit.text()})
        
        self.close()
        
        
    def dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Data")
        layout = QVBoxLayout()
        message = QLabel("You have added a new data")
        record = QLabel("Song: "+self.songLineEdit.text()+" Artist: "+self.artistLineEdit.text()+" Writen by: "+self.writenByLineEdit.text()+" Soucre: "+self.soucreLineEdit.text()+" Times: "+self.timesLineEdit.text()+" Rating: "+self.ratingLineEdit.text()+" Listen: "+self.listenLineEdit.text())

        layout.addWidget(message)
        layout.addWidget(record)
        dialog.setModal(True)
        dialog.resize(300, 200)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setLayout(layout)
        dialog.exec_()
        

    def reject(self):
        print("Cancelled")
        self.close()

class Read(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.table = QTableView()
        self.label = QLabel("List of All Music" )
        conn = connect()
        data = pd.DataFrame(list(conn.find())).drop(['_id'],axis=1)
        self.model = TableModel(data)
        self.table.setModel(self.model)
        layout.addWidget(self.table)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(800, 600)
        self.show()
        self.close()

class Update(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Data")
        self.setGeometry(150, 150, 250, 150)
        self.layout = QVBoxLayout()
        self.label = QLabel("Update Data")
        self.formGroupBox = QGroupBox("Form")
        self.choose = QListWidget()
        self.choose.addItems(["Song","Artist"])
        self.oldItem = QLineEdit()
        self.newItem = QLineEdit()
        self.createForm()


        self.choose.itemClicked.connect(self.chooseItem)
        self.oldItem.editingFinished.connect(self.oldItemChanged)
        self.newItem.editingFinished.connect(self.newItemChanged)

        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.formGroupBox)
        
        self.setLayout(self.layout)
        
    def chooseItem(self):
        print(self.choose.currentItem().text())
        if self.choose.currentItem().text():
            self.oldItem.show()
            self.newItem.hide()
    def oldItemChanged(self):
        print(self.oldItem.text())
        if self.oldItem.text():
            self.newItem.show()

    def newItemChanged(self):
        print(self.newItem.text())
        if self.newItem.text():
            self.buttons = QDialogButtonBox()
            self.buttons.setStandardButtons(
                QDialogButtonBox.StandardButton.Cancel
                | QDialogButtonBox.StandardButton.Ok
            )
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)
            self.layout.addWidget(self.buttons)

    def accept(self):
        print("Accepted")
        print(self.oldItem.text())
        print(self.newItem.text())
        self.updateRecord()
        self.close()
        
    

    def updateRecord(self):
        conn = connect()
        print(self.choose.currentItem().text())
        if self.choose.currentItem().text() == "Song":
            conn.update_one({"Song":str(self.oldItem.text())},{"$set":{"Song":str(self.newItem.text())}})
        elif self.choose.currentItem().text() == "Artist":
            conn.update_one({"Artist":str(self.oldItem.text())},{"$set":{"Artist":str(self.newItem.text())}})
        self.dialog()

    def reject(self):
        print("Cancelled")
        self.close()
        
    def createForm(self):
  
        # creating a form layout
        formLayout = QFormLayout()
        formLayout.addRow(QLabel("Select field:"),self.choose)
        formLayout.addRow(QLabel("Old:"),self.oldItem)
        formLayout.addRow(QLabel("New:"), self.newItem)
        
       
        # setting layout
        self.formGroupBox.setLayout(formLayout)

    def dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Data")
        layout = QVBoxLayout()
        message = QLabel("You have Update a data")
        record = QLabel("From "+self.oldItem.text()+" to "+self.newItem.text())

        layout.addWidget(message)
        layout.addWidget(record)
        dialog.setModal(True)
        dialog.resize(300, 200)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setLayout(layout)
        dialog.exec_()
        
class Delete(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Data")
        self.setGeometry(150, 150, 250, 150)
        self.layout = QVBoxLayout()
        self.label = QLabel("Delete By")
        self.formGroupBox = QGroupBox("Form")
        self.choose = QListWidget()
        self.choose.addItems(["Song","Artist"])
        self.item = QLineEdit()
        self.createForm()
        
        self.choose.itemClicked.connect(self.chooseItem)
        self.item.editingFinished.connect(self.itemChanged)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.formGroupBox)

        self.setLayout(self.layout)
        
    def createForm(self):
              
          # creating a form layout
          formLayout = QFormLayout()
          formLayout.addRow(QLabel("Select field:"),self.choose)
          formLayout.addRow(QLabel("Item:"),self.item)
        
          # setting layout
          self.formGroupBox.setLayout(formLayout)
    def chooseItem(self):
        print(self.choose.currentItem().text())
        if self.choose.currentItem().text():
            self.item.show()
    def itemChanged(self):
        print(self.item.text())
        if self.item.text():
            self.buttons = QDialogButtonBox()
            self.buttons.setStandardButtons(
                QDialogButtonBox.StandardButton.Cancel
                | QDialogButtonBox.StandardButton.Ok
            )
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)
            self.layout.addWidget(self.buttons)
    def accept(self):
        print("Accepted")
        print(self.item.text())
        self.deleteRecord()
        self.close()
    def deleteRecord(self):
        conn = connect()
        if self.choose.currentItem().text() == "Song":
            conn.delete_one({"Song":str(self.item.text())})
        elif self.choose.currentItem().text() == "Artist":
            conn.delete_one({"Artist":str(self.item.text())})
        self.dialog()
    def reject(self):
        print("Cancelled")
        self.close()
    def dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Data")
        layout = QVBoxLayout()
        message = QLabel("You have Delete a data")
        record = QLabel("Item: "+self.item.text())

        layout.addWidget(message)
        layout.addWidget(record)
        dialog.setModal(True)
        dialog.resize(300, 200)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setLayout(layout)
        dialog.exec_()
        
    
class Analytic(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setGeometry(1200, 1200,1400, 1600)
        self.label = QLabel("Show analytic")
        layout.addWidget(self.label)
        sc1 = MplCanvas(self, width=5, height=4, dpi=100)
        sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        sc3 = MplCanvas(self, width=5, height=4, dpi=100)
        conn = connect()
        df = pd.DataFrame(list(conn.find())).drop("_id",axis=1)
        df = df.loc[df['Time'] != ''].loc[df['Rating'] != ''].loc[df['Listen'] != '']
        df['Rating'] = df['Rating'].astype('float')
        df['Time'] = df['Time'].astype('float')
        sc1.axes.plot(df.groupby('Artist').agg({"Rating":'mean',"Time":"mean"}))
        sc1.axes.set_title("Mean Rating and Time")
        sc1.axes.set_xlabel("Artist")
        sc1.axes.set_ylabel("Rating and Time")
        sc2.axes.plot(df.groupby('Artist').agg({"Listen":'sum'}))
        sc2.axes.set_title("Total Listen")
        sc2.axes.set_xlabel("Artist")
        sc2.axes.set_ylabel("Listen")
        sc3.axes.plot(df.groupby('Artist').agg({"Song":'count'}))
        sc3.axes.set_title("Total Song")
        sc3.axes.set_xlabel("Artist")
        sc3.axes.set_ylabel("Song")

        layout.addWidget(sc1)
        layout.addWidget(sc2)
        layout.addWidget(sc3)
        self.setLayout(layout)
        

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.

        self.window1 = Create()
        self.window2 = Read()
        self.window3 = Update()
        self.window4 = Delete()
        self.window5 = Analytic()
        self.setWindowTitle("Manage Data")
        self.setGeometry(500, 300, 300, 300)
        helloMsg = QLabel("Choose Function")
        helloMsg.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        
        layout = QVBoxLayout()
        layout.addWidget(helloMsg)
        self.button1 = QPushButton("Create")
        self.button1.clicked.connect(self.toggle_window1)
        layout.addWidget(self.button1)
        


        self.button2 = QPushButton("Read")
        self.button2.clicked.connect(self.toggle_window2)
        layout.addWidget(self.button2)
        

        self.button3 = QPushButton("Update")
        self.button3.clicked.connect(self.toggle_window3)
        layout.addWidget(self.button3)
        

        self.button4 = QPushButton("Delete")
        self.button4.clicked.connect(self.toggle_window4)
        layout.addWidget(self.button4)
        

        self.button5 = QPushButton("Analytic")
        self.button5.clicked.connect(self.toggle_window5)
        layout.addWidget(self.button5)

        self.button6 = QPushButton("Refresh")
        self.button6.clicked.connect(self.refresh)
        layout.addWidget(self.button6)
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
    def toggle_window1(self):
        if not self.w:
            self.w = self.window1
            self.w.show()
        else:
            self.w.close()
            self.w = None
    def toggle_window2(self):
        if not self.w:
            self.w = self.window2
            self.w.show()
        else:
            self.w.close()
            self.w = None
    def toggle_window3(self):
        if not self.w:
            self.w = self.window3
            self.w.show()
        else:
            self.w.close()
            self.w = None
    def toggle_window4(self):
        if not self.w:
            self.w = self.window4
            self.w.show()
        else:
            self.w.close()
            self.w = None
    def toggle_window5(self):
        if not self.w:
            self.w = self.window5
            self.w.show()
        else:
            self.w.close()
            self.w = None
    def refresh(self):
        self.window1 = Create()
        self.window2 = Read()
        self.window3 = Update()
        self.window4 = Delete()
        self.window5 = Analytic()
        self.w = None
        



            
        
    
    
   
        
        

    


if __name__ == '__main__':
    while True:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()
        

