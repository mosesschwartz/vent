#!/usr/bin/env python
# encoding: utf-8
"""
PacketDetailTree.py

Created by Moses Schwartz on 2009-11-13.
Copyright (c) 2009 . All rights reserved.
"""

import sys
import os

import psml

from PyQt4.QtCore import * 
from PyQt4.QtGui import *

class PacketDetailTree(QTreeView):
    def __init__(self, *args): 
        QTreeView.__init__(self, *args)
    
    def set_data(self, model):
        self.setModel(model)

def main():
    pass


if __name__ == '__main__':
    main()

