"""

@file    tlsprogram.py
@author  Dario Zubillaga
@date    2014-04-1

Python script that generates a TLSPrograms file which includes: 
- id: The traffic light id as it is on the sumo network.
- foes: A list of lists with the lanes linked together in a traffic
        light phase.
- phaseTime: A list with the phase time for every phase defined in
        the foes list.
All this information is retrieved from the SUMO network with the use of the sumolib.net library.

"""

import argparse, sys
sys.path.append('/usr/share/sumo/tools')
import traci, sumolib.net

def parse():
  parser = argparse.ArgumentParser(description="Generate a SUMO map with a new numeration from an OSM file", 
    epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  general = parser.add_argument_group('General')
  general.add_argument('-n','--net', help='Sumo network', required=True)
  parameters = parser.parse_args()
  return parameters
  
par = parse()
if par.net[-8:] == '.net.xml':
  filename = par.net[:-8]
else:
  print "The file extension has to be .net.xml"
sumonet = sumolib.net.readNet(par.net)
program = open('TLSprograms.txt','w')
for tls in sumonet._tlss:
  this = str(tls.getID())
  for i in range(len(sumonet.getNode(tls.getID())._foes)):
    friends = ''
    j = 0
    c = 0
    for bit in sumonet.getNode(tls.getID())._foes[i]:
      if int(bit) == 1:
	     friends = friends + str(j) + ','
	     c += 1
      j += 1
    friends = str(c*5) + ':' + friends
    this =  this + '\t\t' + friends[:-1]
  this = this + '\n'
  program.write(this)
program.close()
 
    
  
  
