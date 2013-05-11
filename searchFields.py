#!/usr/bin/env python

import sys

from PyQt4 import QtCore, QtGui, uic

class searchTerm(QtGui.QWidget):
    def __init__(self, parent=None, *args):
        super(searchTerm, self).__init__(*args)
        self.parent = parent
        uic.loadUi('designer/searchTerm.ui', self)

#    @QtCore.pyqtSlot()
#    def on_addSearch_clicked(self):
#        print "foo"

    @QtCore.pyqtSlot()
    def on_removeSearch_clicked(self):
        if not self.parent.searchItems.itemAt(1):
            #is there an item at index 1? i.e., more than one term?
            #if not, return!
            return 
            
        print dir(self.parent.searchItems)
        self.parent.searchItems.removeWidget(self)
        self.setParent(None)
        self.parent.searchItems.update()
        del self

    def get_search_terms(self):
        return { 'fieldType' : str(self.fieldType.currentText()), 
                'searchType': str(self.searchType.currentText()), 
                'searchText': str(self.searchText.text()) }

class searchBox(QtGui.QGroupBox):
    def __init__(self, *args):
        super(searchBox, self).__init__(*args)

        uic.loadUi('designer/searchBox.ui', self)

        self.addSearch()

#        print search
#        self.searchItems.addLayout(search)

    def addSearch(self):
        st = searchTerm(self)
        self.searchItems.addWidget(st)
        st.addSearch.clicked.connect(self.addSearch_clicked)
        st.removeSearch.clicked.connect(self.removeSearch_clicked)
        self.searchItems.update()
        print "added search"

    def addSearch_clicked(self, foo):
        print "addSearch Clicked"
        print foo
        self.addSearch()

    def removeSearch_clicked(self):
        self.searchItems.update()
        print "removeSearch Clicked"
        
    def getSearchTerms(self):
        count = self.searchItems.count()
        print "number of terms: ", count
        return [self.searchItems.itemAt(x).widget().get_search_terms() for x in xrange(count)]

    @QtCore.pyqtSlot()
    def on_runSearch_clicked(self):
       print "foo"
       count = self.searchItems.count()
       print "number of terms: ", count
       #[self.searchItems.itemAt(x).widget().get_search_terms() for x in xrange(count)]

    @QtCore.pyqtSlot()
    def on_addSearch_clicked(self):
        print "foo"

def main():
    app = QtGui.QApplication(sys.argv)
    widget = searchBox()
    #st = searchTerm(widget)
    #widget.searchItems.addWidget(st)

    widget.searchItems.update()
    widget.show()
    widget.addSearch()
    sys.exit(app.exec_())

if __name__ == "__main__": 
    main()
