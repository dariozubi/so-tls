"""

@file    setCfg.py
@author  Dario Zubillaga
@date    2014-04-1

Python script that generates the configuration file for SUMO and the output file that it 
uses to retrieve information from the simulation.

"""


import argparse, sys, os
sys.path.append('/usr/share/sumo/tools')
import sumolib.net

def get_net_file_directory(net_file):
  dirname = os.path.split(net_file)[0]
  return dirname

def open_detector_file(destination_dir, detector_file_name):
  return open(os.path.join(destination_dir, detector_file_name), "w")

def parse():
  parser = argparse.ArgumentParser(description="Generate the SUMO configuration file for a specific network", 
    epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  general = parser.add_argument_group('General')
  general.add_argument('-n','--net', help='Network in the OSM format', required=True)
  
  parameters = parser.parse_args()
  return parameters


par = parse()
dirNet = par.net[:-8]
network = sumolib.net.readNet(par.net)
fileout = dirNet + '.out.xml'
outfile = open_detector_file(get_net_file_directory(par.net),fileout)
print >> outfile, '<output>'
print >> outfile, '  <edgeData id="0" freq="10" file="../../output/edges.xml" excludeEmpty="true"/>'
print >> outfile, '  <vTypeProbe id="0" freq="1" file="../../output/vehicles.xml"/>'
for tls in network._tlss:
  print >> outfile, '  <timedEvent type="SaveTLSSwitchTimes" source="{0}" dest="../../output/tls{0}.xml"/>'.format(tls.getID())
print >> outfile, '</output>'
outfile.close()
filesumo = dirNet + '.sumocfg'
configure = open_detector_file(get_net_file_directory(par.net),filesumo)
print >> configure, """<?xml version="1.0" encoding="iso-8859-1"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd">
    <input>
      <net-file value="{0}.net.xml"/>
      <route-files value="{0}.rou.xml"/>
      <additional-files value="{0}.det.xml {0}.out.xml"/>
    </input>
    <output>
      <summary value="../../output/summary.xml"/>
    </output>
    <report>
      <no-warnings value="true"/>
    </report>
    <traci_server>
      <remote-port value="8813" />
    </traci_server>
    <time-to-teleport value="-1" />
</configuration>""".format(dirNet)
configure.close()
filesumo2 = dirNet + '2.sumocfg'
configure2 = open_detector_file(get_net_file_directory(par.net),filesumo2)
print >> configure2, """<?xml version="1.0" encoding="iso-8859-1"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd">
    <input>
      <net-file value="{0}.net.xml"/>
      <route-files value="{0}.rou.xml"/>
      <additional-files value="{0}.det2.xml {0}.out.xml"/>
    </input>
    <output>
      <summary value="../../output/summary.xml"/>
    </output>
    <report>
      <no-warnings value="true"/>
    </report>
    <traci_server>
      <remote-port value="8813" />
    </traci_server>
    <time-to-teleport value="-1" />
</configuration>""".format(dirNet)
configure2.close()
