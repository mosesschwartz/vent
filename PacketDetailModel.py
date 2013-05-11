#!/usr/bin/env python
# encoding: utf-8
"""
PacketDetailModel.py

Created by Moses Schwartz on 2009-11-13.
Copyright (c) 2009 . All rights reserved.
"""

from PyQt4.QtCore import * 
from PyQt4.QtGui import *

class PacketDetailModel(QAbstractItemModel):    
    def __init__(self, tree, parent=None, *args): 
        QAbstractItemModel.__init__(self, parent, *args) 
        self.packet = tree[0]
        self.parent_map = dict((c, p) for p in self.packet.getiterator() for c in p)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()
            
        item = index.internalPointer()

        column = index.column()
        if column == 0:
            if role == Qt.DisplayRole:
                showname = item.get("showname")
                if showname is None:
                    showname = item.get("name")
                return QVariant(showname)
        return QVariant()
        
    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.packet
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem[row]
        
        if childItem != None:
            return self.createIndex(row, 0, childItem)
        else:
            return QModelIndex()
         
    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        childItem = child.internalPointer()

        parentItem = self.parent_map[childItem]

        if parentItem == self.packet:
            return QModelIndex()

        grand_parent = self.parent_map[parentItem]
        parent_row = list(grand_parent).index(parentItem)

        return self.createIndex(parent_row, 0, parentItem)

    def rowCount(self, parent):
        if not parent.isValid():
            parentItem = self.packet
        else:
            parentItem = parent.internalPointer()
        
        rc = len(list(parentItem))
        return rc
    
    def columnCount(self, parent):
        return 1
 
    def headerData(self, section, orientation, role):
        '''if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return QVariant(self.tr("Name"))
            elif section == 1:
                return QVariant(self.tr("Attributes"))
            elif section == 2:
                return QVariant(self.tr("Value"))
            else:
                return QVariant()'''

        return QVariant()

def main():
	print "Model classes. Must be imported..."


if __name__ == '__main__':
	main()

