#!/usr/bin/env python
"""
@file    runner.py 
@author  Dario Zubillaga
@date    2014-04-1

Main python script that controls a SUMO simulation using the SUMO's traci module.
The script starts a SUMO simulation using the files included in the input/network 
directory which includes a net file (net.xml), road file (rou.xml), two detectors
files (det.xml, det2.xml), an output file (out.xml), a configuration file (.sumocfg)
and a tls programs file. Once initialized the traci module is used to retrieve 
information from the detectors and switch the lights of the traffic lights using
different algorithms.

"""

import subprocess, sys, math, time
import tls, init, parameters
sys.path.append('"C:/Program Files (x86)/DLR/Sumo/tools"')
import traci

par = parameters.parse()
PORT = 8813   

print("Initializing parameters...")
init.tlsParameters(par)
if par.tls == 1:
  cfgType = ''
else:
  cfgType = '2'

print("Reading TLS programs...")
tlsRead = init.readTLSPrograms(par.tlsPrograms, par.dirNet)
tlsList = {}
for tl in tlsRead:
  if par.tls == 0:
    tlsList[tl[0]] = tls.trafficlight(tl[0],tl[1],tl[2])
  elif par.tls == 1:
    tlsList[tl[0]] = tls.selforg(tl[0],tl[1],tl[2])
  elif par.tls == 2:
    tlsList[tl[0]] = tls.prevcycles(tl[0],tl[1],tl[2])
  elif par.tls == 3:
    tlsList[tl[0]] = tls.queue(tl[0],tl[1],tl[2])
print 'Network file done'

#Llamada a sumo con traci
if not traci.isEmbedded():
  if par.gui:
    sumoBinary = "sumo-gui.exe"
    cfgType = "3"
  else:
    sumoBinary = "sumo.exe" 
  print("Using "+sumoBinary+"...")
  sumoConfig = 'input/'+par.dirNet+'/'+par.dirNet+cfgType+'.sumocfg'
  sumoProcess = subprocess.Popen('"C:/Program Files (x86)/DLR/Sumo/bin/{:s}" -c {:s}'.format(sumoBinary, sumoConfig), shell=True, stdout=sys.stdout)
  traci.init(PORT)

  # Loop principal
print 'Main Loop'
tlsIDList = traci.trafficlights.getIDList()
step = 0
while (step == 0 or traci.simulation.getMinExpectedNumber() > 0) and step < 60000:
  traci.simulationStep()
  step += 1
  for i in tlsIDList:
    tlsList[i].switchLight()
traci.close()
sys.stdout.flush()
time.sleep(15)
# init.renameFiles(par.dirNet,par.tls,par.dataNum,tlsIDList)