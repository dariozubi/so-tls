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

Python script that generates detectors in every street used for the generation of 
traffic flows for DFROUTER SUMO's tool

SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
Copyright (C) 2009-2013 DLR (http://www.dlr.de/) and contributors
All rights reserved
"""

import logging
import optparse
import os
import sys
import xml.dom.minidom
sys.path.append('/usr/share/sumo/tools')
import sumolib.net

def get_net_file_directory(net_file):
    """ Returns the directory containing the net file given. """

    dirname = os.path.split(net_file)[0]
    return dirname

def open_detector_file(destination_dir, detector_file_name):
    """ Opens a new detector file in given directory. """

    return open(os.path.join(destination_dir, detector_file_name), "w")

def adjust_detector_length(requested_detector_length,
                           requested_distance_to_tls,
                           lane_length):
    """ Adjusts requested detector's length according to
        the lane length and requested distance to TLS.

        If requested detector length is negative, the resulting detector length
        will match the distance between requested distance to TLS and lane
        beginning.
        

        If the requested detector length is positive, it will be adjusted
        according to the end of lane ending with TLS: the resulting length
        will be either the requested detector length or, if it's too long
        to be placed in requested distance from TLS, it will be shortened to
        match the distance between requested distance to TLS
        and lane beginning. """

    if requested_detector_length == -1:
        return lane_length - requested_distance_to_tls
        
    return min(lane_length - requested_distance_to_tls,
               requested_detector_length)

def adjust_detector_position(final_detector_length,
                             requested_distance_to_tls,
                             lane_length):
    """ Adjusts the detector's position. If the detector's length
        and the requested distance to TLS together are longer than
        the lane itself, the position will be 0; it will be 
        the maximum distance from lane end otherwise (taking detector's length
        and requested distance to TLS into accout). """

    return max(0,
        lane_length - final_detector_length - requested_distance_to_tls)
      
if __name__ == "__main__":
    # pylint: disable-msg=C0103

    logging.basicConfig(level="INFO")

    option_parser = optparse.OptionParser()
    option_parser.add_option("-n", "--net-file",
                         dest="net_file",
                         help="Network file to work with. Mandatory.",
                         type="string")
    option_parser.add_option("-l", "--detector-length",
                         dest="requested_detector_length",
                         help="Length of the detector in meters "
                              "(-1 for maximal length).",
                         type="int",
                         default=250)
    option_parser.add_option("-d", "--distance-to-TLS",
                         dest="requested_distance_to_tls",
                         help="Distance of the detector to the traffic "
                              "light in meters. Defaults to 0.1m.",
                         type="float",
                         default=.1)
    option_parser.add_option("-f", "--frequency",
                         dest="frequency",
                         help="Detector's frequency. Defaults to 60.",
                         type="int",
                         default=60)
    option_parser.add_option("-o", "--output",
                         dest="output",
                         help="The name of the file to write the detector "
                              "definitions into. Defaults to e1.add.xml.",
                         type="string",
                         default="e1.add.xml")
    option_parser.add_option("-r", "--results-file",
                         dest="results",
                         help="The name of the file the detectors write "
                              "their output into. Defaults to e1output.xml.",
                         type="string",
                         default="e1output.xml")
    option_parser.set_usage("routeDetectors.py -n example.net.xml "
                        "-l 250 -d .1 -f 60")

    (options, args) = option_parser.parse_args()
    if not options.net_file:
        print "Missing arguments"
        option_parser.print_help()
        exit()

    logging.info("Reading net...")
    net = sumolib.net.readNet(options.net_file)
    
    logging.info("Generating detectors...")
    detectors_xml = xml.dom.minidom.Element("detectors")
    lanes_with_detectors = set()
    for edge in net._edges:
        for lane in edge._lanes:
            lane_length = lane.getLength()
            lane_id = lane.getID()
            
            logging.debug("Creating detector for lane %s" % (str(lane_id)))

            if lane_id in lanes_with_detectors:
                logging.warn("Detector for lane %s already generated" %
                    (str(lane_id)))
                continue           

            lanes_with_detectors.add(lane_id)

            final_detector_length = adjust_detector_length(
                options.requested_detector_length,
                options.requested_distance_to_tls,
                lane_length)
            final_detector_position = adjust_detector_position(
                final_detector_length,
                options.requested_distance_to_tls,
                lane_length)

            detector_xml = xml.dom.minidom.Element("detectorDefinition")
            detector_xml.setAttribute("id", "det_" + str(lane_id))
            detector_xml.setAttribute("lane", str(lane_id))
            detector_xml.setAttribute("pos", str(final_detector_position))
            #detector_xml.setAttribute("freq", str(options.frequency))
	    #detector_xml.setAttribute("file", str(options.results))
            detectors_xml.appendChild(detector_xml)

    detector_file = open_detector_file(
        get_net_file_directory(options.net_file),
        options.output)
    detector_file.write(detectors_xml.toprettyxml())
    detector_file.close()

    logging.info("%d e1 detectors generated!" % len(lanes_with_detectors))

