#!/usr/bin/env python
"""
@file    parseResults.py 
@author  Dario Zubillaga
@date    2014-04-1

Python "module" that process the results obtained in the simulations and applies
the different information measures. It uses the graphMaker.R script to generate
graphs if wanted.

"""

import xml.etree.ElementTree as ET
import argparse
import math
import sys
import subprocess
import os
sys.path.append('/home/dariozubillaga/Descargas/sumo-0.20.0/tools')
# sys.path.append('/usr/share/sumo/tools')
import sumolib.net
from datetime import date, time, datetime, timedelta

"""
@function parse
@author  Dario Zubillaga

Parses the command line arguments for the script

"""


def parse():
    parser = argparse.ArgumentParser(description="Parse results from a SUMO simulation",
                                     epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    general = parser.add_argument_group('General')
    general.add_argument(
        '-n', '--dir', help="File directory of the results (usually the network's name", required=True)
    general.add_argument(
        '-s', '--sim', help='Simulation number which is going to be parsed', required=True)
    general.add_argument('-g', '--graphs', action='store_true',
                         help='Generate graphs and put them in ../graphs/directory')
    general.add_argument('-b', '--base', type=int,
                         help='Base for the normalization', default=10)
    general.add_argument('-u', '--update', type=int, help='Size of the update interval for the Shannon information',
                         default=100)
    parameters = parser.parse_args()
    return parameters

"""
@function normalize
@author  Dario Zubillaga

Normalizes the input data in the infoBase.

"""


def normalize(data, infoBase):
    base = infoBase
    minData = min(data)
    maxData = max(data)
    normData = []
    if maxData - minData > 0:
        for i in range(len(data)):
            normData.append(
                int(math.floor(base * (data[i] - minData) / (maxData - minData))))
    else:
        for i in range(len(data)):
            normData.append(0)
    return normData

"""
@function shannon
@author  Dario Zubillaga

Uses the normalize function to obtain the shannon information of the input data
in the infoBase.

"""


def shannon(data, infoBase):
    base = infoBase
    normData = normalize(data, infoBase)
    H = 0
    pr = []
    for i in range(base):
        pr.append(0)
    for i in normData:
        if i != 0:
            pr[i - 1] += 1
        else:
            pr[0] += 1
    for i in range(base):
        pr[i] = float(pr[i]) / len(normData)
        if pr[i] > 0:
            H += pr[i] * math.log(pr[i], 2)
    return -H / math.log(base, 2)

"""
@function makeGraph
@author  Dario Zubillaga

Calls the graphMaker script to create a graph of the data

"""


def makeGraph(directory, name, result, column):
    subprocess.call("Rscript ../graphs/graphMaker.R {0} {1} {2} {3}".format(
        directory, name, result, column), shell=True)

"""
@function streets
@author  Dario Zubillaga

Parses the xml simulation results into a new file containing the shannon information
measured as the time between cars in every street in the network

"""


def streets(par, method):
    detectorFile = '{0}/streets_{2}_{1}.xml'.format(par.dir, par.sim, method)
    tree = ET.parse(detectorFile)
    root = tree.getroot()
    street = {}
    streetInfo = {}
    firstTime = 0
    for interval in root.iter('interval'):
        time = float(interval.get("begin"))
        if float(interval.get('nVehContrib')) != 0:
            id = interval.get('id')
            if id in street:
                if len(street[id]) > 0:
                    lastTime = street[id][-1]
                    street[id].append(time - lastTime)
                else:
                    street[id].append(time - firstTime)
            else:
                firstTime = time
                street[id] = []
        if time % par.update == 0 and time != 0:
            id = interval.get('id')
            if id in street:
                if id in streetInfo:
                    if len(street[id]) > 2:
                        streetInfo[id].append(shannon(street[id], par.base))
                else:
                    streetInfo[id] = []
                    if len(street[id]) > 2:
                        streetInfo[id].append(shannon(street[id], par.base))
    for id in streetInfo:
        if len(streetInfo[id]) > 0:
            filename = 'street{0}_{1}_{2}.txt'.format(id[5:], method, par.sim)
            streetFile = open('{0}/{1}'.format(par.dir, filename), 'w')
            for element in streetInfo[id]:
                line = '{:.10f}\n'.format(element)
                streetFile.write(line)
            streetFile.close()
            if par.graphs:
                makeGraph(par.dir, filename, 'Information', 1)

"""
@function intersections
@author  Dario Zubillaga

Parses the xml simulation results into a new file containing the shannon information
measured as the time between cars in every intersection in the network

"""


def intersections(par, method):
    detectorFile = '{0}/intersections_{2}_{1}.xml'.format(
        par.dir, par.sim, method)
    tree = ET.parse(detectorFile)
    root = tree.getroot()
    intersection = {}
    intersectionInfo = {}
    firstTime = 0
    for interval in root.iter('interval'):
        time = float(interval.get("begin"))
        if float(interval.get('vehicleSum')) != 0:
            id = interval.get('id').split('_')[1]
            if id in intersection:
                if len(intersection[id]) > 0:
                    lastTime = intersection[id][-1]
                    intersection[id].append(time - lastTime)
                else:
                    intersection[id].append(time - firstTime)
            else:
                firstTime = time
                intersection[id] = []
        if time % par.update == 0 and time != 0:
            id = interval.get('id').split('_')[1]
            if id in intersection:
                if id in intersectionInfo:
                    if len(intersection[id]) > 2:
                        intersectionInfo[id].append(
                            shannon(intersection[id], par.base))
                else:
                    intersectionInfo[id] = []
                    if len(intersection[id]) > 2:
                        intersectionInfo[id].append(
                            shannon(intersection[id], par.base))
    for id in intersectionInfo:
        if len(intersectionInfo[id]) > 0:
            filename = 'intersection{0}_{1}_{2}.txt'.format(
                id, method, par.sim)
            intersectionFile = open('{0}/{1}'.format(par.dir, filename), 'w')
            for element in intersectionInfo[id]:
                line = '{:.10f}\n'.format(element)
                intersectionFile.write(line)
            intersectionFile.close()
            if par.graphs:
                makeGraph(par.dir, filename, 'Information', 1)

"""
@function streets
@author  Dario Zubillaga

Parses the xml simulation results into a new file containing the occupancy,
waiting time and speed in each street (edge) of the network

"""


def edges(par, network):
    edgesFile = '{3}{0}/edges_{2}_{1}.xml'.format(par.dir, par.sim, method, outputDir)
    tree = ET.parse(edgesFile)
    root = tree.getroot()
    priority = {}
    total = [0, [0], [0], [0]]
    for interval in root.iter('interval'):
        for edge in interval.iter('edge'):
            edgeId = edge.get('id')
            id = network.getEdge(edgeId)._priority
            total[0] += 1
            if (edge.get('occupancy') != None):
              total[1][-1] += float(edge.get('occupancy'))
              total[2][-1] += float(edge.get('waitingTime'))
              total[3][-1] += float(edge.get('speed'))
              if id in priority:
                  priority[id][0] += 1
                  priority[id][1][-1] += float(edge.get('occupancy'))
                  priority[id][2][-1] += float(edge.get('waitingTime'))
                  priority[id][3][-1] += float(edge.get('speed'))
              else:
                  priority[id] = [0, [0], [0], [0]]
        if total[0] != 0:
            dividend = total[0]
        else:
            dividend = 1
        total[1][-1] /= dividend
        total[2][-1] /= dividend
        total[3][-1] /= dividend
        total[1].append(0)
        total[2].append(0)
        total[3].append(0)
        for id in priority:
            if priority[id][0] != 0:
                dividend = priority[id][0]
            else:
                dividend = 1
            priority[id][1][-1] /= dividend
            priority[id][2][-1] /= dividend
            priority[id][3][-1] /= dividend
            priority[id][0] = 0
            priority[id][1].append(0)
            priority[id][2].append(0)
            priority[id][3].append(0)
    filename = 'edges_{0}.csv'.format(method)
    totalEdgeFile = open('{2}{0}/{1}'.format(par.dir, filename, outputDir), 'a')
    if (par.sim == "20"):
        totalEdgeFile.write("Hour,Simulation,Occupancy,Waiting Time,Speed\n")
    d = date(2017,12,20)
    t = time(6,0)
    start = datetime.combine(d,t)
    d = date(2017,12,20)
    t = time(22,0)
    end = datetime.combine(d,t)
    i = 0
    while (start < end):
        line = '{},{},{:.10f},{:.10f},{:.10f}\n'.format(
            start,par.sim+"%",total[1][i], total[2][i], total[3][i])
        start = start + timedelta(0,60)
        i = i+1
        totalEdgeFile.write(line)
    totalEdgeFile.close()
    if par.graphs:
        makeGraph(par.dir, filename, 'Occupancy', 1)
        makeGraph(par.dir, filename, 'WaitingTime', 2)
        makeGraph(par.dir, filename, 'Speed', 3)
    # for id in priority:
        #filename = 'edge_priority{0}_{1}_{2}.txt'.format(id,method,par.sim)
        #prioritiesFile = open('{0}/{1}'.format(par.dir,filename),'w')
        # for i in range(len(priority[id][1])):
        #line = '{:.10f}\t{:.10f}\t{:.10f}\n'.format(priority[id][1][i],priority[id][2][i],priority[id][3][i])
        # prioritiesFile.write(line)
        # prioritiesFile.close()
        # if par.graphs:
        # makeGraph(par.dir,filename,'Occupancy',1)
        # makeGraph(par.dir,filename,'WaitingTime',2)
        # makeGraph(par.dir,filename,'Speed',3)


# def speed(par, network, outputDir):
#     vehiclesFile = '{3}{0}/vehicles_{2}_{1}.xml'.format(
#         par.dir, par.sim, method, outputDir)
#     tree = ET.parse(vehiclesFile)
#     root = tree.getroot()
#     totalLength = 0
#     print("root loaded")
#     filename = 'vehicles_total_{0}_{1}.csv'.format(method, par.sim)
#     totalVehicleFile = open('{2}{0}/{1}'.format(par.dir, filename, outputDir), 'w')
#     for edge in network.getEdges():
#         totalLength += edge.getLength() * len(edge._lanes)
#     for timestep in root.iter('timestep'):
#         tempSpeed = 0
#         vehicleNumber = 0
#         for vehicle in timestep.iter('vehicle'):
#             vehicleSpeed = vehicle.get('speed')
#             tempSpeed += float(vehicleSpeed)
#             vehicleNumber += 1
#         if vehicleNumber != 0:
#             velocity = tempSpeed / vehicleNumber
#             density = vehicleNumber * 7.5 / totalLength
#         else:
#             velocity = 0
#             density = 0
#         line = '{:.10f},{:.10f}\n'.format(density[i], velocity[i])
#         totalVehicleFile.write(line)
#     totalVehicleFile.close()

def speedLarge(par, network, outputDir):
    # vehiclesFile = '{3}{0}/vehicles_{2}_{1}.xml'.format(
    #     par.dir, par.sim, method, outputDir)
    # context = ET.iterparse(vehiclesFile, events=('start', 'end'))
    # context = iter(context)
    # event, root = context.next()
    totalLength = 0
    # c = 0
    # filename = 'vehicles_{0}.csv'.format(method)
    # totalVehicleFile = open('{2}{0}/{1}'.format(par.dir, filename, outputDir), 'a')
    # d = date(2017,12,20)
    # t = time(6,0)
    # start = datetime.combine(d,t)
    # d = date(2017,12,20)
    # t = time(22,1)
    # end = datetime.combine(d,t)
    # if (par.sim == "20"):
    #     totalVehicleFile.write('Hour,Simulation,Density,Velocity\n')
    for edge in network.getEdges():
        totalLength += edge.getLength() * len(edge._lanes)
    print(totalLength);
    # for event, elem in context:
    #     tempSpeed = 0
    #     if event == "end" and elem.tag == "timestep":
    #       vehicleNumber = 0
    #       velocity = 0
    #       density = 0
    #       for vehicle in elem.iter('vehicle'):
    #           vehicleSpeed = vehicle.get('speed')
    #           tempSpeed += float(vehicleSpeed)
    #           vehicleNumber += 1
    #       if vehicleNumber != 0:
    #           velocity = tempSpeed / vehicleNumber
    #           density = vehicleNumber * 7.5 / totalLength
    #       else:
    #           velocity = 0
    #           density = 0
    #       if start<end:
    #         line = '{},{},{:.10f},{:.10f}\n'.format(start,par.sim+"%",density, velocity)
    #         totalVehicleFile.write(line)
    #       start = start + timedelta(0,60)
    #       c=c+1
    #       root.clear()
    # totalVehicleFile.close()

"""
@function switches
@author  Dario Zubillaga

Parses the xml simulation results into a new file containing the shannon information
measured as the time between switches of every traffic light in the network

"""


def switches(par, network, method):
    switchInfo = {}
    for tls in network._tlss:
        tlsFile = '{0}/tls{2}_{3}_{1}.xml'.format(
            par.dir, par.sim, tls.getID(), method)
        tree = ET.parse(tlsFile)
        root = tree.getroot()
        phases = {}
        for tlsSwitch in root.iter('tlsSwitch'):
            fromLane = tlsSwitch.get('fromLane')
            toLane = tlsSwitch.get('toLane')
            id = fromLane + toLane
            if id in phases:
                phases[id].append(float(tlsSwitch.get('duration')))
            else:
                phases[id] = []
            if id in switchInfo:
                if len(phases[id]) > 2:
                    switchInfo[id].append(shannon(phases[id], par.base))
            else:
                switchInfo[id] = []
    for id in switchInfo:
        if len(switchInfo[id]) > 0:
            filename = 'switches{0}_{1}_{2}.txt'.format(id, method, par.sim)
            switchesFile = open('{0}/{1}'.format(par.dir, filename), 'w')
            for element in switchInfo[id]:
                line = '{:.10f}\n'.format(element)
                switchesFile.write(line)
            switchesFile.close()
            if par.graphs:
                makeGraph(par.dir, filename, 'Information', 1)

par = parse()
if os.path.basename(os.getcwd()) == 'src':
    dirnet = 'input/{0}/{0}.net.xml'.format(par.dir)
    outputDir = 'output/'
else:
    dirnet = '../input/{0}/{0}.net.xml'.format(par.dir)
    outputDir = ''
network = sumolib.net.readNet(dirnet)
tlsType = {0: 'fixed', 1: 'selforg', 2: 'prevcyc', 3: 'queue'}
method = tlsType[0]
# print("Parsing fixed edges...")
# edges(par,network)
print("Parsing fixed vehicles...")
speedLarge(par, network, outputDir)
# method = tlsType[1]
# print("Parsing selforg edges...")
# edges(par,network)
# print("Parsing selforg vehicles...")
# speedLarge(par, network, outputDir)

