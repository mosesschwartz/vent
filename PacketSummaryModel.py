#!/usr/bin/env python
# encoding: utf-8
"""
PacketSummaryModel.py

Created by Moses Schwartz on 2009-11-13.
Copyright (c) 2009 . All rights reserved.
"""

from PyQt4.QtCore import * 
from PyQt4.QtGui import *
 
class PacketSummaryModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
 
        self.row_bg_colors = {
            'ARP': '#D6E8FF',
            'ICMP': '#C2C2FF',
            'SMB': '#FFFA99',
            'HTTP': '#8DFF7F',
            'IPX': '#FFE3E5',
            'TCP': '#E7E6FF',
            'UDP': '#70E0FF',}
 
    def run_search(self, searchField, searchType, searchTerm):
        number = 0
        time = 1
        src = 2
        dest = 3
        proto = 4
        info = 4

        for packet in arraydata:
            if searchType is "is":
                pass

    def get_arraydata(self):
        return self.arraydata

    def get_frame(self, row):
        return self.arraydata[row][0]
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        else:
            data = self.arraydata[index.row()][index.column()] 

        if role == Qt.DisplayRole: 
            return QVariant(self.arraydata[index.row()][index.column()])  

        if role == Qt.BackgroundRole:
            proto = self.arraydata[index.row()][4]
            try:
                color = self.row_bg_colors[ proto ]
            except KeyError:
                color = "#FFFFFF"
            return QVariant(QBrush(QColor( color )))


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        #elif orientation == Qt.Vertical and role == Qt.DisplayRole:
        #    return QVariant(col+1)
        return QVariant()


def main():
	print "Model classes. Must be imported..."


if __name__ == '__main__':
	main()

