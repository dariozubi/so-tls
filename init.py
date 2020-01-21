#!/usr/bin/env python
"""
@file    init.py 
@author  Dario Zubillaga
@date    2014-04-1

Python "module" that contains functions to initialize the trafficlights 
for the runner.py script

"""

import tls, subprocess


"""
@function readTLSPrograms
@author  Dario Zubillaga

Read an external .txt file to define every traffic light through 
a list of three items:
- id: The traffic light id as it is on the sumo network.
- foes: A list of lists with the lanes linked together in a traffic
        light phase.
- phaseTime: A list with the phase time for every phase defined in
        the foes list.

"""
def readTLSPrograms(name, dirNet):
  tlsFile = str('input\\'+dirNet+'\\'+name)
  with open(tlsFile) as par:
    content = par.readlines()
  par.close()
  tl = []
  i = 0
  for line in content:
    if '#' in line:
      continue
    else:
      foes = []
      phaseTime = []
      tl.append([])
      c = 0
      for element in line.split():
      	if line.split().index(element) == 0:
      	  id = str(element)
      	else:
      	  for subelement in element.split(':'):
      	    if element.split(':').index(subelement) == 0:
      	      phaseTime.append(int(subelement))
      	    else:
      	      foes.append([])
      	      for lane in subelement.split(','):
                foes[c].append(int(lane))
              c += 1
        # phaseTime.append(30)
    tl[i].append(id)
    tl[i].append(foes)
    tl[i].append(phaseTime)
    i += 1
  return tl

"""
@function tlsParameters
@author  Dario Zubillaga

Defines the parameters for the traffic light classes

"""
def tlsParameters(par):
  tls.trafficlight.sumonet = str('input\\'+par.dirNet+'\\'+par.dirNet+'.net.xml')
  if par.tls == 1:
    tls.selforg.tr = par.treshold
    tls.selforg.miniTr = par.miniTreshold
    tls.selforg.tmin = par.phaseMin
  if tls == 2:
    tls.prevcycles.cycles = par.cycles

"""
@function renameFiles
@author  Dario Zubillaga

Renames the output files and puts them in the right directory

"""
def renameFiles(net,tlsType,dataNum,tlsList):
  name = {0:'fixed',1:'selforg',2:'prevcyc',3:'queue'}
  # cmd = 'mv output/edges.xml output/{0}/edges_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  cmd = 'move output\\edges.xml output\\{0}\\edges_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  subprocess.call(cmd,shell=True)
  # cmd = 'mv output/summary.xml output/{0}/summary_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  # cmd = 'move output\\summary.xml output\\{0}\\summary_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  # subprocess.call(cmd,shell=True)
  # cmd = 'mv output/streets.xml output/{0}/streets_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  # cmd = 'move output\\streets.xml output\\{0}\\streets_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  # subprocess.call(cmd,shell=True)
  # cmd = 'mv output/vehicles.xml output/{0}/vehicles_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  cmd = 'move output\\vehicles.xml output\\{0}\\vehicles_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  subprocess.call(cmd,shell=True)
  # cmd = 'mv output/intersections.xml output/{0}/intersections_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  # cmd = 'move output\\intersections.xml output\\{0}\\intersections_{1}_{2}.xml'.format(net,name[tlsType],dataNum)
  #subprocess.call(cmd,shell=True)
  # for i in tlsList:
    # cmd = 'mv output/tls{3}.xml output/{0}/tls{3}_{1}_{2}.xml'.format(net,name[tlsType],dataNum,i)
    # cmd = 'move output\\tls{3}.xml output\\{0}\\tls{3}_{1}_{2}.xml'.format(net,name[tlsType],dataNum,i)
    # subprocess.call(cmd,shell=True)
  # cmd = 'rm input/{0}/e3detector.xml'.format(net)
  cmd = 'del input\\{0}\\e3detector.xml'.format(net)
  subprocess.call(cmd,shell=True)
  