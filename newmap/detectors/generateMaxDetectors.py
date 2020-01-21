#!/usr/bin/env python
"""
@originalfile    generateTLSE3Detectors.py 
@author  Daniel Krajzewicz
@author  Karol Stosiek
@author  Michael Behrisch
@date    2007-10-25
@version $Id: generateTLSE3Detectors.py 14425 2013-08-16 20:11:47Z behrisch $

@modification  Dario Zubillaga
@date          2014-04-10

Python script that generates detectors of the size of the street for every street 
whitin a traffic light intersection0

SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
Copyright (C) 2009-2013 DLR (http://www.dlr.de/) and contributors
All rights reserved
"""


import logging 
import optparse
import os
import sys
import xml.dom.minidom

# sys.path.append('/usr/share/sumo/tools')
sys.path.append('"C:/Program Files (x86)/DLR/Sumo/tools"')
import sumolib.net

def get_net_file_directory(net_file):
  dirname = os.path.split(net_file)[0]
  return dirname

def open_detector_file(destination_dir, detector_file_name):
  return open(os.path.join(destination_dir, detector_file_name), "w")
  
def nextEdge(fromNode, toNode):
  nodeType = network.getNode(fromNode)._type
  if nodeType != 'right_before_left':
    (fromN, toN) = (fromNode,toNode)
    return '{0}to{1}'.format(fromN,toN)
  else:
    for edge in network.getNode(fromNode).getIncoming():
      if edge.getID() !='{0}to{1}'.format(toNode,fromNode):
	fromN, toN = edge.getID().split('to')
	return nextEdge(fromN, toN)
  
if __name__ == "__main__":
  option_parser = optparse.OptionParser()
  option_parser.add_option("-n", "--net-file",dest="net_file",help="Network file to work with. Mandatory.",
    type="string")
  option_parser.add_option("-f", "--frequency",dest="frequency",help="Detector's frequency. Defaults to 1.",type="int",
    default=1)
  option_parser.add_option("-o", "--output",dest="output",
    help="The name of the file to write the detector definitions into. Defaults to detectors.det.xml.",type="string",
    default="detectors.det.xml")
  option_parser.add_option("-r", "--results-file",dest="results",
    help="The name of the file the detectors write their output into. Defaults to e1output.xml.",type="string",
    default="e3detector.xml")
  option_parser.set_usage("generateMaxDetectors.py -n example.net.xml -l 250 -d .1 -f 60")
  (options, args) = option_parser.parse_args()
  
  if not options.net_file:
      print "Missing arguments"
      option_parser.print_help()
      exit()
      
  network = sumolib.net.readNet(options.net_file)
  detectors = xml.dom.minidom.Element("detectors")
  for tls in network._tlss:
    for edge in sorted(tls.getEdges(), key=sumolib.net.edge.Edge.getID):
      detector = xml.dom.minidom.Element("entryExitDetector")
      detector.setAttribute("id", "det_" + str(tls._id) + "_" + str(edge.getID()))
      detector.setAttribute("freq", str(options.frequency))
      detector.setAttribute("file", "../../output/intersections.xml")
      fromNode, toNode = edge.getID().split('to')
      entry = str(nextEdge(fromNode,toNode))
      for lane in network.getEdge(entry)._lanes:
	detectorEntry = xml.dom.minidom.Element("detEntry")
	detectorEntry.setAttribute("lane", str(lane.getID()))
	detectorEntry.setAttribute("pos", "10")
	detector.appendChild(detectorEntry)
      for lane in edge._lanes:
	detectorExit = xml.dom.minidom.Element("detExit")
	detectorExit.setAttribute("lane", str(lane.getID()))
	detectorExit.setAttribute("pos", "-1")
	detector.appendChild(detectorExit)
      detectors.appendChild(detector)
  edge_with_detectors = set()
  for edge in network._edges:
    position = edge.getLength()/2
    if edge.getID() in edge_with_detectors:
      continue
    edge_with_detectors.add(edge.getID())
    detector_xml = xml.dom.minidom.Element("inductionLoop")
    detector_xml.setAttribute("file", "../../output/streets.xml")
    detector_xml.setAttribute("freq", "1")
    detector_xml.setAttribute("friendlyPos", "x")
    detector_xml.setAttribute("id", "info_" + str(edge.getID()))
    detector_xml.setAttribute("lane", str(edge._lanes[0].getID()))
    detector_xml.setAttribute("pos", str(position))
    detectors.appendChild(detector_xml)
  detector_file = open_detector_file(get_net_file_directory(options.net_file),options.output)
  detector_file.write(detectors.toprettyxml())
  detector_file.close()

