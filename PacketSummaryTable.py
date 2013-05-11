#!/usr/bin/env python
# encoding: utf-8
"""
PacketSummaryTable.py

Created by Moses Schwartz on 2009-11-13.
Copyright (c) 2009 . All rights reserved.
"""

import sys
import os

import psml

from PyQt4.QtCore import * 
from PyQt4.QtGui import *

class PacketSummaryTable(QTableView):
    def __init__(self, *args): 
        QTableView.__init__(self, *args)

        # set the minimum size
#        self.setMinimumSize(800, 500)

        # show grid
        self.setShowGrid(True)

        # hide vertical header
        vh = self.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.horizontalHeader()
        hh.setStretchLastSection(True)
    
        # Set the selection behavior to only allow selection of entire rows
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def set_data(self, model):
        self.setModel(model)

        # set column width to fit contents
        self.resizeColumnsToContents()

        # set row height
        nrows = model.rowCount(0)
        for row in xrange(nrows):
            self.setRowHeight(row, 18)


def main():
	pass


if __name__ == '__main__':
	main()

