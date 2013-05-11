import sys 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from PyQt4.uic import *

import psml
import tshark
 
#from modeltest import ModelTest
from PacketSummaryModel import PacketSummaryModel
from PacketDetailModel import PacketDetailModel

from PacketSummaryTable import PacketSummaryTable
from PacketDetailTree import PacketDetailTree
 
from histogram import Histogram, TermDistViz

from searchFields import searchBox, searchTerm
 
def main(): 
    app = QApplication(sys.argv) 
    w = MainWindow() 
    w.show() 
    sys.exit(app.exec_()) 



class QuitButton(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

#        self.setGeometry(300, 300, 250, 150)

        quit = QPushButton('Close', self)
 #       quit.setGeometry(10, 10, 60, 35)

        self.connect(quit, SIGNAL('clicked()'),
            qApp, SLOT('quit()'))


class FilterInput(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        filterButton = self.createButton("&Filter", self.run_filter)
        searchButton = self.createButton("&Search", self.run_search)

#        addButton = self.createButton("+", self.add_search_field)
#        delButton = self.createButton("-", self.del_search_field)

        self.filterComboBox = self.createComboBox()
        self.searchComboBox = self.createComboBox()

        filterLabel = QLabel("Filter:")
        searchLabel = QLabel("Search:")
        

        sourceLabel = QLabel("Source")
        destLabel = QLabel("Destination")
        protoLabel = QLabel("Protocol")
        infoLabel = QLabel("Info")

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()

        mainLayout = QVBoxLayout()
        


        showFilterBox = False
        if (showFilterBox):
            filterGroupBox = QGroupBox("PCAP Filter")

            filterLayout = QHBoxLayout()
            filterLayout.addWidget(self.filterComboBox)
            filterLayout.addWidget(filterButton)
            filterGroupBox.setLayout(filterLayout)

            mainLayout.addWidget(filterGroupBox)

#        searchGroupBox = QGroupBox("Packet Search")
        
#        searchLayout = QHBoxLayout()
#        searchLayout.addWidget(searchLabel)
#        searchLayout.addWidget(self.searchComboBox)
#        searchLayout.addWidget(searchButton)
        
#        searchGroupBox.setLayout(searchLayout)
        self.sb = searchBox()
        mainLayout.addWidget(self.sb)

#        spacer = QSpacerItem(1,200)
 #       mainLayout.addSpacerItem(spacer)

        self.setLayout(mainLayout)
        
        

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def run_search(self):
        print "search"
    
    def run_filter(self, filterText):
        filterText = self.filterComboBox.currentText()
        self.updateComboBox(self.filterComboBox)
#        w.ts.set_filter
        qApp.activeWindow().ts.set_filter(str(filterText))
        qApp.activeWindow().updateWidgets()
        

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QSizePolicy.Expanding,
                QSizePolicy.Preferred)
        return comboBox
        
    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

class MainWindow(QMainWindow): 
    def __init__(self, *args): 
        QMainWindow.__init__(self, *args) 

        self.make_menus()

        self.statusBar = self.statusBar()
        self.statusBar.showMessage("VENT")
        self.setWindowTitle(self.tr("VENT"))

        
        self.packet_summary_table = PacketSummaryTable()

        self.packet_detail_tree = PacketDetailTree()
        
        self.filter_input = FilterInput()
 #       self.filter_input = QDockWidget()
#        self.filter_input.setWidget(self.filter_input_widget)
        
        self.histogram = TermDistViz()
        
        vsplitter = QSplitter()
        vsplitter.setOrientation(Qt.Vertical)
        
        hsplitter = QSplitter()
        hsplitter.setOrientation(Qt.Horizontal)
        
        vsplitter.addWidget(self.histogram)
        vsplitter.addWidget(self.packet_summary_table) 
        vsplitter.addWidget(self.packet_detail_tree)
        
#        splitter.setMinimumSize(QSize(650,600))
        hsplitter.addWidget(vsplitter)
        hsplitter.addWidget(self.filter_input)
        
        self.setCentralWidget(hsplitter)

        self.setBaseSize(900,600)
#        self.addDockWidget(Qt.RightDockWidgetArea, self.filter_input)

        self.test()
      


        
#        self.connect(fileSelectionModel, SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), SLOT("test_slot()"))
#        self.connect(fileSelectionModel, SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.updateSelection)

    def connections(self):
        fileSelectionModel = QItemSelectionModel(self.summary_model, self.packet_summary_table)
        self.packet_summary_table.setSelectionModel(fileSelectionModel)
        fileSelectionModel.currentChanged.connect(self.get_packet_detail)
#        self.filter_input.
        self.filter_input.sb.runSearch.clicked.connect(self.runSearch)
        
        self.histogram.vs.valueChanged.connect(self.packet_summary_table.verticalScrollBar().setValue)
        self.packet_summary_table.verticalScrollBar().valueChanged.connect(self.histogram.vs.setValue)
        
    def get_packet_detail(self,model_index_a,model_index_b):
        frame = self.summary_model.get_frame(model_index_a.row())
        self.detail_model = self.get_detail_model(frame)
        self.packet_detail_tree.set_data(self.detail_model)
        
    def make_menus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.tr("&Open..."), self.openFile,
                                QKeySequence(self.tr("Ctrl+O")))
        self.fileMenu.addAction(self.tr("E&xit"), self, SLOT("close()"),
                                QKeySequence(self.tr("Ctrl+Q")))

    def minimumSize(self):
        '''Does nothing for MainWindow, just keeping this around so I remember it for other widgets later'''
        return QSize(800,920)

    def test(self):
        pcap_file = '1k.pcap'
        self.ts = tshark.TShark(pcap_file)
        
        self.summary_model = self.get_summary_model()
        self.packet_summary_table.set_data(self.summary_model)
        
        self.detail_model = self.get_detail_model(1)
        self.packet_detail_tree.set_data(self.detail_model)    
        
        self.histogram.set_data(self.summary_model)
        
        self.connections()    

    def get_detail_model(self, frame_number):
        details = self.ts.get_frame_details(frame_number)
        parsed_details = psml.load_pdml(details)
        pdt_model = PacketDetailModel(parsed_details)
        #self.modeltest = ModelTest(pdt_model, self);
        return pdt_model

    def get_summary_model(self):
        summary = self.ts.get_summary()
        parsed_summary = psml.load_psml(summary)
        tabledata = psml.make_table(parsed_summary)
        #print tabledata
        header = ['No.', 'Time', 'Source', 'Destination', 'Protocol', 'Info']

        tm = PacketSummaryModel(tabledata, header, self)
        return tm

    def updateWidgets(self):
        self.summary_model = self.get_summary_model()
        self.packet_summary_table.set_data(self.summary_model)
        
        self.connections()
#        self.detail_model = self.get_detail_model(1)
 #       self.packet_detail_tree.set_data(self.detail_model)
    

    
    def runSearch(self):
        terms = self.filter_input.sb.getSearchTerms()
        self.histogram.set_data(self.summary_model)
        self.histogram.run_search(terms)

        
        print "RUN RUN RUN"

    def openFile(self):
        file_path = QFileDialog.getOpenFileName(self, "Open File",
            self.pcap_file, "PCAP files (*.pcap)")

        if not file_path.isEmpty():
            pcap_file = str(file_path)

            self.ts = tshark.TShark(pcap_file)
            self.mainWindow.packet_summary_table.set_data(self.ts)
            self.mainWindow.packet_detail_tree.set_data(self.ts,1)



if __name__ == "__main__": 
    main()
