#!/usr/bin/env python
"""
@originalfile    generateTLSE3Detectors.py 
@author  Daniel Krajzewicz
@author  Karol Stosiek
@author  Michael Behrisch
@date    2007-10-25
@version $Id: generateTLSE3Detectors.py 14425 2013-08-16 20:11:47Z behrisch $

@modification  Dario Zubillaga
@date          2014-04-1

Python script that generates the three detectors needed for the self-organized
algorithm of Gershenson

SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
Copyright (C) 2009-2013 DLR (http://www.dlr.de/) and contributors
All rights reserved
"""

import logging
import optparse
import os
import sys
import xml.dom.minidom

sys.path.append('/home/dariozubillaga/Descargas/sumo-0.20.0/tools')
import sumolib.net

def get_net_file_directory(net_file):
  dirname = os.path.split(net_file)[0]
  return dirname

def open_detector_file(destination_dir, detector_file_name):
  return open(os.path.join(destination_dir, detector_file_name), "w")

if __name__ == "__main__":
  option_parser = optparse.OptionParser()
  option_parser.add_option("-n", "--net-file",dest="net_file",help="Network file to work with. Mandatory.",
    type="string")
  option_parser.add_option("-k", "--detector-k-length",dest="requested_k_detector_length",
    help="Length of the k detector in meters (-1 for maximal length).",type="int",default=50)
  option_parser.add_option("-m", "--detector-m-length",dest="requested_m_detector_length",
    help="Length of the m detector in meters light in meters. Defaults to 0.1m.",type="float",default=15)
  option_parser.add_option("-e", "--detector-e-length",dest="requested_e_detector_length",
    help="Length of the e detector in meters light in meters. Defaults to 0.1m.",type="float",default=10)
  option_parser.add_option("-f", "--frequency",dest="frequency",help="Detector's frequency. Defaults to 1.",type="int",
    default=1)
  option_parser.add_option("-o", "--output",dest="output",
    help="The name of the file to write the detector definitions into. Defaults to detectors.det.xml.",type="string",
    default="detectors.det.xml")
  option_parser.add_option("-r", "--results-file",dest="results",
    help="The name of the file the detectors write their output into. Defaults to e1output.xml.",type="string",
    default="e3detector.xml")
  option_parser.set_usage("generateSplitDetectors.py -n example.net.xml -l 250 -d .1 -f 60")
  (options, args) = option_parser.parse_args()
  
  if not options.net_file:
      print "Missing arguments"
      option_parser.print_help()
      exit()

  network = sumolib.net.readNet(options.net_file)
  detectors_xml = xml.dom.minidom.Element("detectors")
  for tls in network._tlss:
      for edge in sorted(tls.getEdges(), key=sumolib.net.edge.Edge.getID):
	  for lane in edge._lanes:
	    kdetector = xml.dom.minidom.Element("laneAreaDetector")
	    kdetector.setAttribute("id", "k_" + str(lane.getID()))
	    kdetector.setAttribute("lane", str(lane.getID()))
	    if options.requested_k_detector_length > lane.getLength():
	      klength = lane.getLength()
	      kpos = 0
	    else:
	      klength = options.requested_k_detector_length
	      kpos = lane.getLength() - klength -1
	    kdetector.setAttribute("length", str(klength))
	    kdetector.setAttribute("pos", str(kpos))
	    # kdetector.setAttribute("freq", str(options.frequency))
	    # kdetector.setAttribute("file", str(options.results))
	    kdetector.setAttribute("cont", 'False')
	    mdetector = xml.dom.minidom.Element("laneAreaDetector")
	    mdetector.setAttribute("id", "m_" + str(lane.getID()))
	    mdetector.setAttribute("lane", str(lane.getID()))
	    if options.requested_m_detector_length > lane.getLength():
	      mlength = lane.getLength()
	      mpos = 0
	    else:
	      mlength = options.requested_m_detector_length
	      mpos = lane.getLength() - mlength -1
	    mdetector.setAttribute("length", str(mlength))
	    mdetector.setAttribute("pos", str(mpos))
	    # mdetector.setAttribute("freq", str(options.frequency))
	    # mdetector.setAttribute("file", str(options.results))
	    mdetector.setAttribute("cont", 'False')
	    detectors_xml.appendChild(kdetector)
	    detectors_xml.appendChild(mdetector)
	 
      lanes_with_detectors = set()
      for connection in tls._connections:
	  lane = connection[1]
	  lane_length = lane.getLength()
	  lane_id = lane.getID()        
	  if lane_id in lanes_with_detectors:
	    continue   
	  lanes_with_detectors.add(lane_id)
	  detector_xml = xml.dom.minidom.Element("inductionLoop")
	  # detector_xml.setAttribute("file", options.results)
	  # detector_xml.setAttribute("freq", str(options.frequency))
	  detector_xml.setAttribute("friendlyPos", "x")
	  detector_xml.setAttribute("id", "e_" + str(lane_id))
	  detector_xml.setAttribute("lane", str(lane_id))
	  detector_xml.setAttribute("pos", str(options.requested_e_detector_length))
	  detectors_xml.appendChild(detector_xml)
	
  edge_with_detectors = set()
  for edge in network._edges:
    position = edge.getLength()/2
    if edge.getID() in edge_with_detectors:
      continue
    edge_with_detectors.add(edge.getID())
    detector_xml = xml.dom.minidom.Element("inductionLoop")
    detector_xml.setAttribute("file", "../../output/streets.xml")
    # detector_xml.setAttribute("freq", "1")
    detector_xml.setAttribute("friendlyPos", "x")
    detector_xml.setAttribute("id", "info_" + str(edge.getID()))
    detector_xml.setAttribute("lane", str(edge._lanes[0].getID()))
    detector_xml.setAttribute("pos", str(position))
    detectors_xml.appendChild(detector_xml)
      

  detector_file = open_detector_file(get_net_file_directory(options.net_file),options.output)
  detector_file.write(detectors_xml.toprettyxml())
  detector_file.close()

