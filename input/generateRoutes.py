#!/usr/bin/env python
"""
@file    generateRoutes.py 
@author  Dario Zubillaga
@date    2014-04-1

Python script that generates routes for an specific network contained in a same named 
directory. It counts both the number of incoming  and outgoing streets in the network 
to stablish the number of possible routes for cars outside the network to be taken. 
Then it generates flows from this information for DUAROUTER to use.

"""


# THERE'S A PROBLEM WITH THE GENERATION OF INTERVALS. THEY'RE NOT APPEARING IN THE FILE *.FLOWS.XML AND MAYBE IS THE REASON WHY DUAROUTER THROWS SOME ERRORS

import sys, subprocess, os, argparse, math, random
import xml.etree.ElementTree as ET
#sys.path.append('/usr/share/sumo/tools')
# sys.path.append('/home/dariozubillaga/Descargas/sumo-0.20.0/tools')
sys.path.append('"C:/Program Files (x86)/DLR/Sumo/tools"')
import sumolib.net

def parse():
  parser = argparse.ArgumentParser(description="Generate routes and vehicles for a specific network", 
    epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  general = parser.add_argument_group('General')
  general.add_argument('-n','--name', help='Directory name')
  general.add_argument('-f','--flow', default='-1', help="Use current flows file with the input list of flows id's as priority")
  general.add_argument('-t','--time', type=int, default=30, help='Time interval for the cars to come in the simulation in minutes')
  general.add_argument('-c','--cars', type=int, default=1, help='Average number of cars per minute in each priority route')
  parameters = parser.parse_args()
  return parameters
  
par = parse()
if par.flow != '-1':
  ids = par.flow.split(',')
endTime = par.time*60
netName = par.name + '.net.xml'
directory = os.path.dirname(os.path.realpath(__file__))
network = sumolib.net.readNet(directory+'\\'+par.name+'\\'+netName)
inStreets = list()
outStreets = list()
for edge in network.getEdges():
  if edge.is_fringe():
    if len(edge.getIncoming()) == 0:
      inStreets.append(edge.getID())
    elif len(edge.getOutgoing()) == 0:
      outStreets.append(edge.getID())

if par.flow == '-1':
  doc = open(directory+'\\'+par.name+'\\'+par.name+'.flows.xml','w')
  doc.write('<flows>\n')
  doc.write(' <interval begin="0" end="{:d}">\n'.format(endTime))
  i = 0
  for mainNode in inStreets:
    for secondaryNode in outStreets:
      main,dump = mainNode.split('to')
      dump2,secondary = secondaryNode.split('to')
      if mainNode != secondaryNode and main != secondary:
	carNo = random.randint(1,par.time)
	doc.write('  <flow id="{:d}" from="{:s}" to="{:s}" number="{:d}"/>\n'.format(i,mainNode,secondaryNode,carNo))
	i += 1
  doc.write(' </interval>\n')
  doc.write('</flows>')
  doc.close()

else:
  tree = ET.parse(directory+'/'+par.name+'/'+par.name+'.flows.xml')
  root = tree.getroot()
  for flow in root.iter('flow'):
    if flow.get('id') in ids:
      flow.set('number',str(random.randint(1,par.time)*par.cars))
    else:
      flow.set('number',str(random.randint(1,par.time)))
  tree.write(directory+'\\'+par.name+'\\'+par.name+'.flows.xml')
  
# subprocess.call('duarouter -f {1}/{0}/{0}.flows.xml -n {1}/{0}/{0}.net.xml -o {1}/{0}/{0}.rou.xml --randomize-flows --ignore-errors'.format(par.name,directory), shell=True)
subprocess.call('duarouter -r {1}/{0}/{0}.flows.xml -n {1}/{0}/{0}.net.xml -o {1}/{0}/{0}.rou.xml --randomize-flows --ignore-errors'.format(par.name,directory), shell=True)
