"""

@file    newMap.py
@author  Dario Zubillaga
@date    2014-04-1

Python script that changes an OSM file into a SUMO network file with new names for the nodes
and edeges using NETCONVERT. It also creates the detectors files, the configuration file and
the TLSPrograms file based on the network and saves it in a directory with the network name.

Based on http://sumo.dlr.de/wiki/Networks/Import/OpenStreetMap

"""

import argparse, subprocess, os
import xml.etree.ElementTree as ET

def parse():
  parser = argparse.ArgumentParser(description="Generate a SUMO map with a new numeration from an OSM file or another SUMO network", 
    epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("network", help='Network file')
  network = parser.add_mutually_exclusive_group()
  network.add_argument('-n','--net', action='store_true', help='The network is in the OSM format')
  network.add_argument('-s','--sumo', action='store_true', help='The network is in the SUMO format')
  parser.add_argument('-e','--edit', action='store_true', help='Use sumo-gui')
  parameters = parser.parse_args()
  return parameters
  
def changeNames(filename):
  nodes = ET.parse('{0}.nod.xml'.format(filename))
  edges = ET.parse('{0}.edg.xml'.format(filename))
  connections = ET.parse('{0}.con.xml'.format(filename))
  tls = ET.parse('{0}.tll.xml'.format(filename))
  nodeRoot = nodes.getroot()
  edgeRoot = edges.getroot()
  conRoot = connections.getroot()
  tlsRoot = tls.getroot()
  i=0
  for node in nodeRoot.iter('node'):
    nodeId = node.get('id')
    for tl in tlsRoot.iter('tlLogic'):
      if tl.get('id') == nodeId:
	tl.set('id','{:d}'.format(i))
    for con in tlsRoot.iter('connection'):
      if con.get('tl') == nodeId:
	con.set('tl','{:d}'.format(i))
    for edge in edgeRoot.iter('edge'):
      if edge.get('from') == nodeId:
	edge.set('from','{:d}'.format(i))
      if edge.get('to') == nodeId:
	edge.set('to','{:d}'.format(i))
    node.set('id','{:d}'.format(i))
    if node.get('type') == 'traffic_light':
      node.set('tl','{:d}'.format(i))
    i+=1
  for edge in edgeRoot.iter('edge'):
    edgeId = edge.get('id')
    name = '{:s}to{:s}'.format(edge.get('from'),edge.get('to'))
    del edge.attrib['type']
    for conn in conRoot.iter('connection'):
      if conn.get('from') == edgeId:
	conn.set('from',name)
      if conn.get('to') == edgeId:
	conn.set('to',name)
    for tll in tlsRoot.iter('connection'):
      if tll.get('from') == edgeId:
	tll.set('from',name)
      if tll.get('to') == edgeId:
	tll.set('to',name)
    edge.set('id',name)
  nodes.write('{0}.nod.xml'.format(filename))
  edges.write('{0}.edg.xml'.format(filename))
  connections.write('{0}.con.xml'.format(filename))
  tls.write('{0}.tll.xml'.format(filename))

par = parse()
if not par.network:
  par.print_help()
  exit()
elif par.network[-4:] == '.osm':
  filename = par.network[:-4]
elif par.network[-8:] == '.net.xml':
  filename = par.network[:-8]
else:
  print "The only options are .osm and .net.xml files"

if par.net:
  print("Create files from OSM with Netconvert...")
  netconvert = 'netconvert --osm-files {0}.osm --geometry.remove --junctions.join --no-turnarounds --plain-output-prefix {0}'.format(filename)
  subprocess.call(netconvert, shell=True)
  changeNames(filename)

if par.sumo:
  print("Create files from SUMO with Netconvert...")
  netconvert = 'netconvert -s {0}.net.xml --no-turnarounds --plain-output-prefix {0}'.format(filename)
  subprocess.call(netconvert, shell=True)
  changeNames(filename)
  
if not par.edit:
  print("Create net file with Netconvert...")
  netconvert = 'netconvert -n {0}.nod.xml -e {0}.edg.xml -x {0}.con.xml -i {0}.tll.xml -o {0}.net.xml --no-turnarounds'.format(filename)
  subprocess.call(netconvert, shell=True)
  print("Detectors script 1...")
  detectors = 'python detectors/generateArealDetectors.py -n {0}.net.xml -o {0}.det.xml'.format(filename)
  subprocess.call(detectors, shell=True)
  print("Detectors script 2...")
  detectors2 = 'python detectors/generateDetectors.py -n {0}.net.xml -o {0}.det2.xml'.format(filename)
  subprocess.call(detectors2, shell=True)
  # subprocess.call('rm {0}.con.xml {0}.edg.xml {0}.nod.xml {0}.tll.xml'.format(filename), shell=True)
  print("Remove non-used files...")
  subprocess.call('del {0}.con.xml {0}.edg.xml {0}.nod.xml {0}.tll.xml {0}.typ.xml'.format(filename), shell=True)
  print("Traffic lights program script...")
  tlsprograms = 'python tlss/tlsProgram.py -n {0}.net.xml'.format(filename)
  subprocess.call(tlsprograms, shell=True)
  print("Configuration file script...")
  sumocfg = 'python outputcfg/setCfg.py -n {0}.net.xml'.format(filename)
  subprocess.call(sumocfg, shell=True)
  if not os.path.isdir('..\\input\\{0}'.format(filename)):
    print("New input folder...")
    # subprocess.call('mkdir ../input/{0}'.format(filename), shell=True)
    subprocess.call('mkdir ..\\input\\{0}'.format(filename), shell=True)
  if not os.path.isdir('..\\output\\{0}'.format(filename)):
    print("New output folder...")
    # subprocess.call('mkdir ../output/{0}'.format(filename), shell=True)
    subprocess.call('mkdir ..\\output\\{0}\\'.format(filename), shell=True)
  print("Move files...")
  # move = 'mv {0}.net.xml ../input/{0}/|mv {0}.det.xml ../input/{0}/|mv {0}.det2.xml ../input/{0}/|mv TLSprograms.txt ../input/{0}'.format(filename)
  move = 'move {0}.net.xml ..\\input\\{0}\\ && move {0}.det.xml ..\\input\\{0}\\ && move {0}.det2.xml ..\\input\\{0}\\ && move TLSprograms.txt ..\\input\\{0}'.format(filename)
  subprocess.call(move, shell=True)
  # move = 'mv {0}.sumocfg ../input/{0}/|mv {0}2.sumocfg ../input/{0}/|mv {0}.out.xml ../input/{0}/'.format(filename)
  move = 'move {0}.sumocfg ..\\input\\{0}\\ && move {0}2.sumocfg ..\\input\\{0}\\ && move {0}.out.xml ..\\input\\{0}\\'.format(filename)
  subprocess.call(move, shell=True)
  print("Create test route file...")
  routes = "python ..\\input\\generateRoutes.py {0}".format(filename)
  print('Network Files created!')
