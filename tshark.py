#!/usr/bin/env python
# encoding: utf-8
"""
tshark.py

Interface to run tshark and get fancy XML back

Created by Moses Schwartz on 2009-11-07.
Copyright (c) 2009 . All rights reserved.
"""

import subprocess

class TShark:
    def __init__(self, pcap_file, readfilter=None):
        self.pcap_file = pcap_file
        self.filter = readfilter
        self.output_type = 'psml'
    
    def _run_tshark(self):                    
        cmd = []
        cmd.append('tshark')
        cmd.append('-T' + self.output_type) # Output type - PDML or PSML
        cmd.append('-r' + self.pcap_file) # File to read from. This could even be live capture, theoretically...
        if ( (self.filter != None) and (self.filter != '') ):
            cmd.append('-R' + self.filter) # Filter to apply

        print cmd
        ts = subprocess.Popen( cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = ts.communicate()
        return stdout
    
    def get_frame_details(self, frame_number):
        self.output_type = 'pdml'
        self.filter = ' frame.number == ' + str(frame_number)
        return self._run_tshark()

    def get_summary(self):
        self.output_type = 'psml'
        return self._run_tshark()

    def set_filter(self, readfilter):
        self.filter = readfilter
    
def main():
    a = TShark()
    a.run_tshark(pcap_file='test.pcap')


if __name__ == '__main__':
    main()

