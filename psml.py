#!/usr/bin/env python

# Import local copy of ElementTree -- 1.3 Alpha 3 from SVN
import ElementTree1_3a.ElementTree as et

class TSharkSummaryPacket:
    def __init__(self, packet):
        '''Packet should be an ElementTree Element'''
        
        self.no = packet[0].text
        self.time = packet[1].text
        self.src = packet[2].text
        self.dst = packet[3].text
        self.proto = packet[4].text
        self.info = packet[5].text
    
    def get_no(self):
        return self.no
    
    def get_time(self):
        return self.time
    
    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst
            
    def get_proto(self):
        return self.proto        

    def get_info(self):
        return self.info

def load_pdml(xmlfile):
    xml_input = et.fromstring(xmlfile)
    return xml_input

def load_psml(xmlfile):
    xml_input = et.fromstring(xmlfile)
    packets = [TSharkSummaryPacket(packet) for packet in xml_input.findall("packet")]
    return packets
    
def make_table(packets):
    data_table = []
    
    for packet in packets:
        packet_summary = [packet.no, packet.time, packet.src, packet.dst, packet.proto, packet.info]
        data_table.append(packet_summary)

    return data_table