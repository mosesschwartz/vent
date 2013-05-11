#!/usr/bin/env python
# encoding: utf-8
"""
gvt.py
graphicsviewtest

Created by Moses Schwartz on 2009-11-08.
Copyright (c) 2009 . All rights reserved.
"""
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
import random



class Histogram(QGraphicsView):
    def __init__(self, parent=None):
        super(Histogram, self).__init__(parent)

        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(0, 0, 600, 100)
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)

        self.setMinimumSize(self.widget_size())
        self.setMaximumSize(self.widget_size())


#        self.widget = QWidget(self)
        self.setStyleSheet("QWidget { background-color: #fff }")
        
#        a,b,c = self.make_polygon()
#        self.scene.addPolygon(a,b,c)

        self.num_polygons = -1
        self.colors = [QColor(255,0,0), QColor(0,255,0), QColor(0,0,255), QColor(255,255,0), QColor(255,0,255), QColor(0,255,255)]

    def widget_size(self):
        return QSize(602,110)
        
    def minimumSize(self):
        return QSize(602,110)

    #def set_data(self, summaryModel):
    #    self.model = summaryModel
    #    self.arraydata = summaryModel.get_arraydata()
    
    def clear_histogram(self):
        for polygon in self.scene.items():
            self.scene.removeItem(polygon)
            self.num_polygons = -1

    def set_data(self, freqs):
        self.clear_histogram()
        for freq_list in freqs:
            a,b,c = self.make_polygon(freq_list)
            self.scene.addPolygon(a,b,c)
        
    def make_polygon(self, frequencies):
        self.num_polygons += 1
        #random_freqs = [n*random.random() for n in [1]*100]
        freq_len = len(frequencies)
        x_positions = range(0, freq_len*6+1, 6)
        points = [QPointF(x_positions[x], 100-100*frequencies[x]) for x in xrange(len(frequencies))]
        points.insert(0, QPointF(-1,100))
        points.append(QPointF(freq_len*6+1, 100))
        foo = QPolygonF(points)
    #    print foo

        color = self.colors[self.num_polygons]
        qp = QPen(color)

        fill_color = QColor(0,0,0)
        fill_color.setAlpha(50)
        fill_brush = QBrush(fill_color, Qt.SolidPattern)

        return foo, qp, fill_brush


class VizScroll(QScrollBar):
    def __init__(self, parent=None):
        super(VizScroll, self).__init__(parent)

        self.setOrientation(Qt.Horizontal)
        self.setFocusPolicy(Qt.StrongFocus)

        self.resize(QSize(642,50))
        self.setMaximum(1000)
        self.setMinimum(0)
        self.setSingleStep(1)
        

        self.setStyleSheet("""
        QScrollBar:horizontal {
             border: 0px;
             background: transparent;
             background-image: url(trans.png);
             opacity: 255;
             height: 0px;
             margin: 0px 0px 0px 0px;
         }
         QScrollBar::handle:horizontal {
             background: transparent;
             opacity: 100;
             min-width: 20px;
             height: 10px;
             margin: 00px 0px 0px 0px;
         }
         QScrollBar::add-line:horizontal {
             border: 2px solid grey;
             background: #32CC99;
             width: 0px;
             subcontrol-position: right;
             subcontrol-origin: margin;
         }
         QScrollBar::sub-line:horizontal {
             border: 2px solid grey;
             background: #32CC99;
             width: 0px;
             subcontrol-position: left;
             subcontrol-origin: margin;
         }""")


class TermDistViz(QWidget):
    def __init__(self, parent=None):
        super(TermDistViz, self).__init__(parent)
    
        self.h = Histogram(parent=self)
 
        self.vs = VizScroll(parent=self.h)
        self.vs.setGeometry(0,0,602,100)

    
#        self.setLayout(self.layout)
    
    def set_data(self, summaryModel):
        self.model = summaryModel
        self.arraydata = summaryModel.get_arraydata()    
    
    def set_histogram(self, histogram):
        self.layout.addWidget(histogram)
        
    def set_slider(self, slider):
        self.layout.addWidget(slider)
        
    def minimumSize(self):
        return QSize(720,220)

    def _freqify(self, occurrences):
        s = 0
        for x in occurrences:
            s+=x
        return float(s) / len(occurrences)

    def _binify(self, occurrences):
        bins = 100
        no_packets = len(occurrences)
        bin_size = float(no_packets) / bins
        import math
        if math.floor(bin_size) == 1:
            return occurrences
        
        bint = int(bin_size)
        freqs = []
        for r in xrange(0,no_packets-bint,bint):
            freqs.append(self._freqify(occurrences[r:r+bint]))
            
        print freqs
        return freqs
        

    def _compare(self, field_index, search_type, search_text):
        field_indexes = {
            'No.' : 0,
            'Time' : 1,
            'Source' : 2,
            'Destination' : 3,
            'Protocol' : 4,
            'Info' : 5
        }
        
        fi = field_indexes[field_index]
        occurs = []
        for ps in self.arraydata:
            if (search_text == None) or (search_text == ''):
                occurs.append(False)
                continue
            try:
                if search_type == 'contains':
                    occurs.append( str(search_text) in str(ps[fi]) )
                elif search_type == 'is':
                    occurs.append( str(search_text) == str(ps[fi]) )
                elif search_type == 'is not':
                    occurs.append( str(search_text) != str(ps[fi]) )
                elif search_type == 'is greater than':
                    occurs.append( str(search_text) > str(ps[fi]) )
                elif search_type == 'is less than':
                    occurs.append( str(search_text) < str(ps[fi]) )
            except:
                occurs.append(False)
        
        int_occurs = [int(x) for x in occurs]
#        print int_occurs
        return self._binify(int_occurs)

    def run_search(self, terms):
        print terms        
        
        search_results = []
        for term in terms:
            search_results.append( self._compare(term['fieldType'], term['searchType'], term['searchText']) )
        
        self.h.set_data(search_results)
        
        #self.h.fitInView(QRectF(0,0,602,100))
            
            
        
        # I need to take these terms, scan through the packet summary model, make lists of frequencies, and pass that to the histogram
        # then tie scrolling through hist to scrolling through packet summary
    

def main():
    app = QApplication(sys.argv)
    widget = TermDistViz()
    widget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

