import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyWidget(QWidget):
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setGrid()
    
    dataLabels = [['a','b','c','d','e','f'], ['ggg','hhh','iii']]
    roles = ['auxiliary', 'constant', 'output', 'time', 'variable']
    labels = []
    comboBoxes = []
    
    def setGrid(self):
        self.showIndex = 0
        self.layout = QVBoxLayout(self)
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        self.updateGrid()
        
        self.changeButton = QPushButton("Change grid")
        self.connect(self.changeButton, SIGNAL("pressed()"), self.updateGrid)
        self.layout.addWidget(self.changeButton)
        
        self.delButton = QPushButton("Delete grid")
        self.connect(self.delButton, SIGNAL("pressed()"), self.deleteGrid)
        self.layout.addWidget(self.delButton)
    
    def deleteGrid(self):
        for i in range(len(self.labels)):
            self.grid.removeWidget(self.labels[i])
            self.grid.removeWidget(self.comboBoxes[i])
            self.labels[i].setParent(None)
            self.comboBoxes[i].setParent(None)
            
        self.labels = []
        self.comboBoxes = []
        self.grid.activate()
    
    def updateGrid(self):
        if self.showIndex == 0:
            self.showIndex = 1
        else:
            self.showIndex = 0
    
        if len(self.labels) > 0:
            self.deleteGrid()
        
        counter = 0
        for text in self.dataLabels[self.showIndex]:
            label = QLabel(text)
            self.grid.addWidget(label, counter, 0)
            self.labels.append(label)
            
            box = QComboBox()
            self.grid.addWidget(box, counter, 1)
            for name in self.roles:
                box.addItem(name) 
            self.comboBoxes.append(box)
            
            counter += 1


def main():
    #print "main start"
    application = QApplication(sys.argv)
    
    mainWindow = QMainWindow()
    application.setActiveWindow(mainWindow)
    mainWindow.resize(400,300)
    mainWindow.show()
    
    widget = MyWidget(mainWindow)
    mainWindow.setCentralWidget(widget)
    
    sys.exit(application.exec_())

    
if __name__ == "__main__":
    main()
