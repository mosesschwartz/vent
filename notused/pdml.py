#!/usr/bin/env python

# Import local copy of ElementTree -- 1.3 Alpha 3 from SVN
import ElementTree1_3a.ElementTree as et

def find_node_attribute_value(attribute, value, parent):
    print parent
    if parent is None: 
        return None
    for node in parent.getchildren():
        if node.attrib[attribute] == value:
            return node
    return None
        
def find_node_named(name, parent):
        find_node_attribute_value("name", name, parent)

class Packet:
    def __init__(self, packet):
        '''Packet should be an ElementTree Element'''
        self.element = packet
        self.summary = self.get_summary(packet)
        self.protos = self.get_protos(packet)
        
        
        
        self.time =  packet.find(".//proto[@name='frame']").find(".//field[@name='frame.time_delta_displayed']").get('show')       
        self.src = packet.find(".//proto[@name='ip']").find(".//field[@name='ip.src']").get("show")
        self.src = packet.find(".//proto[@name='ip']").find(".//field[@name='ip.dst']").get("show")
        self.proto = list(packet.findall("proto"))[-1].get("name")
        print self.proto

        self.seq = None
        self.ack = None
        self.win = None
        self.len = None

        self.info = "Not yet implemented"
    

            
    def get_summary(self, packet):
        summary = {'time':None,'src':None,'dst':None,'proto':None,'info':None}
        
        
    def get_protos(self, packet):
        self.protos = packet.findall('proto')


tree = et.parse("packet.xml")

packets = [Packet(packet) for packet in tree.findall("packet")]
print packets
