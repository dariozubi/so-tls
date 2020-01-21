#!/usr/bin/env python
"""
@file    tls.py 
@author  Dario Zubillaga
@date    2014-04-1

Python module that contains the different classes that represents the different
types of traffic lights to be implemented in the SUMO simulation. 
The main class (trafficlight) defines the fixed time trafficlights. It has:
- The constructor. Defines each traffic light internal variables extracted from
  the tls programs file in the init.py module
- setDetectors method. Sets the number of links in the main class but is used for setting
  the right detectors and other custom variables in the subclasses.
- setStates method. Sets the different states the traffic light may have in a SUMO friendly format
  based on the foes.
- flipTo method. Performs the switch inside the SUMO simulation to change to a new state.
- noflip method. Makes sure SUMO doesn't change the actual state of the traffic light.
- switchLight method. Is the method that performs the actual algorithm of the traffic light based
  on the information read by the detectors or any other heuristic.
The subclasses override the main class methods when needed and usually add a getDetectorsData method
(among others) to retrieve information from the detectors in the SUMO simulation using traci.

In case of adding a new class, it needs at least a constructor with the id, 
foes and phase times as arguments and the switchlight method for the main 
script to work.

"""

import sys
import xml.etree.ElementTree as ET
sys.path.append('/home/dariozubillaga/Descargas/sumo-0.20.0/tools')
# sys.path.append('/usr/share/sumo/tools')
import traci
import sumolib.net


class trafficlight(object):
    sumonet = 'input/delaware/delaware.net.xml'

    def __init__(self, id, foes, phaseTime):
        self.id = str(id)
        self.foes = foes
        self.phases = len(self.foes)
        self.t = 0
        self.tmax = phaseTime
        self.actualPhase = 0
        self.setDetectors()
        self.setStates()

    def setDetectors(self):
        network = sumolib.net.readNet(self.sumonet)
        self.linkNo = len(network._id2tls[self.id].getLinks())

    def setStates(self):
        self.states = []
        for i in range(self.phases):
            st = list('r' * self.linkNo)
            for j in self.foes[i]:
                st[j] = 'g'
            self.states.append(''.join(st))
            # self.states.append('r'*self.linkNo)
        tree = ET.parse(self.sumonet)
        root = tree.getroot()
        for tlLogic in root.iter('tlLogic'):
            if tlLogic.get('id') == self.id:
                for phase in tlLogic.findall('phase'):
                    tlLogic.remove(phase)
                for i in range(len(self.states)):
                    phase = ET.SubElement(tlLogic, 'phase', attrib={
                                          'duration': '{:d}'.format(self.tmax[i]), 'state': self.states[i]})
            tree.write(self.sumonet)

    def flipTo(self, newPhase):
        self.t = 0
        self.actualPhase = newPhase
        traci.trafficlights.setRedYellowGreenState(
            self.id, self.states[newPhase])

    def noflip(self):
        traci.trafficlights.setRedYellowGreenState(
            self.id, self.states[self.actualPhase])

    def switchLight(self):
        self.t += 1
        if self.t > self.tmax[self.actualPhase]:
            newPhase = (self.actualPhase + 1) % self.phases
            self.flipTo(newPhase)
        else:
            self.noflip()

"""
@class trafficlight
@subclass selforg
@author Dario Zubillaga
@date 2014-04-1

Implements a version of the self-organized traffic lights of Gershenson and Rosenblueth in the
paper Self-Organizing Traffic Lights at Multiple-Street Interesections.
The main parameters are:
- tr: threshold for the lanes in red (n in the article)
- miniTr: minimum threshold for the green light to remain green (m in the article)
- tmin: minimum time for the phases
- rules: a list of numbers which determine which rules are going to be applied

"""


class selforg(trafficlight):
    tr = 13
    miniTr = 1
    tmin = 12
    rules = [1, 1, 1, 1, 1, 1]

    def setDetectors(self):
        self.n = [0 for i in range(self.phases)]
        network = sumolib.net.readNet(self.sumonet)
        self.linkNo = len(network._id2tls[self.id].getLinks())
        self.kCars = [0 for i in range(self.linkNo)]
        self.mCars = [0 for i in range(self.linkNo)]
        self.eCars = [0 for i in range(self.linkNo)]
        self.kId = []
        self.mId = []
        self.eId = []
        for i in range(self.linkNo):
            lane = network._id2tls[self.id].getLinks()[i][0][0].getID()
            kDet = 'k' + '_' + lane
            self.kId.append(str(kDet))
            mDet = 'm' + '_' + lane
            self.mId.append(str(mDet))
            elane = network._id2tls[self.id].getLinks()[i][0][1].getID()
            eDet = 'e' + '_' + elane
            self.eId.append(str(eDet))

    def getAreaDetectorsData(self):
        for i in range(self.linkNo):
            eTemp = traci.inductionloop.getLastStepVehicleNumber(self.eId[i])
            temp = 0
            if eTemp > 0:
                temp = traci.inductionloop.getVehicleData(
                    self.eId[i])[0][3] - traci.inductionloop.getVehicleData(self.eId[i])[0][2]
            self.kCars[i] = traci.areal.getJamLengthVehicle(self.kId[i])
            self.mCars[i] = traci.areal.getJamLengthVehicle(self.mId[i])
            if temp > 2:
                self.eCars[i] += 1
            else:
                self.eCars[i] = 0

    # Defines also the n array which contains the number of cars per second in
    # the red phases.
    def setdDetectors(self):
        self.n = [0 for i in range(self.phases)]
        network = sumolib.net.readNet(self.sumonet)
        self.linkNo = len(network._id2tls[self.id].getLinks())
        self.kCars = [0 for i in range(self.linkNo)]
        self.mCars = [0 for i in range(self.linkNo)]
        self.eCars = [0 for i in range(self.linkNo)]
        self.kId = []
        self.mId = []
        self.eId = []
        for i in range(self.linkNo):
            elane = network._id2tls[self.id].getLinks()[i][0][1].getID()
            eDet = 'e_' + elane
            self.eId.append(str(eDet))
            lane = network._id2tls[self.id].getLinks()[i][0][0].getID()
            for edge in network.getTLSSecure(self.id).getEdges():
                for lane2 in edge._lanes:
                    if lane == lane2.getID():
                        kDet = 'k_' + self.id + '_' + edge.getID()
                        mDet = 'm_' + self.id + '_' + edge.getID()
                        self.kId.append(str(kDet))
                        self.mId.append(str(mDet))
                        break

    def getDetectorsData(self):
        for i in range(self.linkNo):
            eTemp = traci.inductionloop.getLastStepVehicleNumber(self.eId[i])
            temp = 0
            if eTemp > 0:
                temp = traci.inductionloop.getVehicleData(
                    self.eId[i])[0][3] - traci.inductionloop.getVehicleData(self.eId[i])[0][2]
            if temp > 2:
                self.eCars[i] += 1
            else:
                self.eCars[i] = 0
            self.kCars[i] = traci.multientryexit.getLastStepVehicleNumber(self.kId[
                                                                          i])
            self.mCars[i] = traci.multientryexit.getLastStepVehicleNumber(self.mId[
                                                                          i])

    def flipTo(self, newPhase):
        trafficlight.flipTo(self, newPhase)
        self.n[newPhase] = 0

    # Flips to the phase whit the maximum n
    def flipMax(self, allred=False):
        # print self.id,'flipMax'
        self.t = 0
        if allred:
            newPhase = self.phases
        else:
            sel = [0 for i in range(self.phases)]
            for i in range(self.linkNo):
                for j in range(self.phases):
                    if i in self.foes[j] and j != self.actualPhase:
                        sel[j] += self.kCars[i]
                        break
            newPhase = sel.index(max(sel))
            # print 'newPhase:', newPhase
        if not allred:
            self.n[newPhase] = 0
        self.actualPhase = newPhase
        traci.trafficlights.setRedYellowGreenState(
            self.id, self.states[newPhase])

    # Uses the next variables to make the decisions:
    # - nG: accumulative number of cars per second whitin a distance d in the green phase
    # - m: number of cars whitin a distance r in the green phase
    # - eG: is different from zero if there's a car upstream the green phase
    # - n: array of accumulative number of cars per second whitin a distance d in the red phases
    # - eR: array in which each index is different from zero if there's a car upstream in the red phases
    def switchLight(self):
        self.t += 1
        # if self.t > self.tmax[self.actualPhase] and self.actualPhase != self.phases:
        # self.flipTo((self.actualPhase+1)%self.phases)
        nG = 0
        m = 0
        eG = 0
        eR = 0
        self.getAreaDetectorsData()
        for i in range(self.linkNo):
            if self.actualPhase == self.phases:
                for j in range(self.phases):
                    if i in self.foes[j]:
                        self.n[j] += self.kCars[i]
                eR += self.eCars[i]
            else:
                if i in self.foes[self.actualPhase]:
                    nG += self.kCars[i]
                    eG += self.eCars[i]
                    m += self.mCars[i]
                else:
                    for j in range(self.phases):
                        if j != self.actualPhase:
                            if i in self.foes[j]:
                                self.n[j] += self.kCars[i]
                                break
                    eR += self.eCars[i]
        # print 'id:',self.id
        # print 'actualPhase:', self.states[self.actualPhase]
        # print 'foes:', self.foes
        # print 'kcars:', self.kCars
        # print 'mcars:', self.mCars
        # print 'ecars:',self.eCars
        # print 'nG:',nG
        # print 'm:', m
        # print 'eG:', eG
        # print 'eR', eR
        # print 'n:',self.n
        # print ''
        temp = [self.n[i] for i in range(self.phases)]
        temp.sort()
        temp.reverse()
        indexes = []
        for i in range(self.phases):
            indexes.append(self.n.index(temp[i]))

        if eG > 0:
            # Just one lane with stopped vehicles is enough (not all)
            if eR > 0:
                if self.rules[5]:
                    self.flipMax(True)
            else:
                if self.rules[4]:
                    self.flipMax()
        elif eR == 0:
            for i in indexes:
                if i != self.actualPhase:
                    if self.rules[5]:
                        if self.actualPhase == self.phases:
                            self.flipMax()
                            break
                    if self.rules[3]:
                        if self.n[i] >= 1 and nG == 0 and self.t >= self.tmin:
                            self.flipTo(i)
                            break
                        elif self.rules[2]:
                            if not (m < self.miniTr and m > 0):
                                if self.rules[1]:
                                    if self.t >= self.tmin:
                                        if self.rules[0]:
                                            if self.n[i] >= self.tr * len(self.foes[i]):
                                                self.flipTo(i)
                                                break
                                else:
                                    if self.n[i] >= self.tr * len(self.foes[i]):
                                        if self.rules[0]:
                                            self.flipTo(i)
                                            break
                    elif self.rules[2]:
                        if not (m < self.miniTr and m > 0):
                            if self.rules[1]:
                                if self.t >= self.tmin:
                                    if self.rules[0]:
                                        if self.n[i] >= self.tr:
                                            self.flipTo(i)
                                            break
                            else:
                                if self.n[i] >= self.tr:
                                    if self.rules[0]:
                                        self.flipTo(i)
                                        break
                    else:
                        if self.rules[1]:
                            if self.t >= self.tmin:
                                if self.rules[0]:
                                    if self.n[i] >= self.tr:
                                        self.flipTo(i)
                                        break
                        else:
                            if self.rules[0]:
                                if self.n[i] >= self.tr:
                                    self.flipTo(i)
                                    break
        else:
            self.noflip()

"""
@class trafficlight
@subclass prevcycles
@author Dario Zubillaga
@date 2014-04-1

Changes each phase duration according to a lineal combination of the previous
cycles. The measured time each cycle is the minimum between the time it takes
for the streets in that phase to be empty and a maximum time defined by the
fixed times of the main class.

"""


class prevcycles(trafficlight):
    cycles = 10

    def setWeights(self):
        self.weights = [1.]
        for i in range(1, self.cycles):
            self.weights.append(self.weights[i - 1] / 2)

    def setDetectors(self):
        self.setWeights()
        self.tmin = 10
        self.timeToEmpty = self.tmax[self.actualPhase]
        self.timeIsSet = False
        self.prevTimes = [
            [10 for i in range(self.cycles)] for j in range(self.phases)]
        network = sumolib.net.readNet(self.sumonet)
        self.linkNo = len(network._id2tls[self.id].getLinks())
        self.detId = []
        for i in range(self.linkNo):
            lane = network._id2tls[self.id].getLinks()[i][0][0].getID()
            for edge in network.getTLSSecure(self.id).getEdges():
                for lane2 in edge._lanes:
                    if lane == lane2.getID():
                        det = 'det_' + self.id + '_' + edge.getID()
                        self.detId.append(str(det))
                        break

    def anyCars(self):
        carNo = 0
        for link in self.foes[self.actualPhase]:
            carNo += traci.multientryexit.getLastStepVehicleNumber(self.detId[
                                                                   link])
        if carNo > 0:
            return True
        else:
            return False

    def updatePrevTimes(self, phase):
        for j in range(1, self.cycles):
            self.prevTimes[phase][j] = self.prevTimes[
                phase][(j + 1) % self.cycles]
        self.prevTimes[phase][0] = self.timeToEmpty

    def setMaxTime(self, newPhase):
        temp = 0
        for i in range(self.cycles):
            temp += self.prevTimes[newPhase][i] * self.weights[i]
        self.tmax[newPhase] = temp

    def switchLight(self):
        self.t += 1
        if self.t > self.tmin and not self.anyCars() and not self.timeIsSet:
            self.timeToEmpty = self.t
            self.timeIsSet = True
        if self.t >= self.tmax[self.actualPhase]:
            self.updatePrevTimes(self.actualPhase)
            newPhase = (self.actualPhase + 1) % self.phases
            self.flipTo(newPhase)
            self.setMaxTime(newPhase)
            self.timeIsSet = False
            self.timeToEmpty = self.tmax[self.actualPhase]
        else:
            self.noflip

"""
@class trafficlight
@subclass queue
@author Dario Zubillaga
@date 2014-04-1

Sets the next phase state according to which street in the states in red
has the most amount of cars (assumed to be the same as the longest queue)

"""


class queue(trafficlight):
    timeCar = 5

    def setDetectors(self):
        network = sumolib.net.readNet(self.sumonet)
        self.linkNo = len(network._id2tls[self.id].getLinks())
        self.detCars = [0 for i in range(self.linkNo)]
        self.detId = []
        for i in range(self.linkNo):
            lane = network._id2tls[self.id].getLinks()[i][0][0].getID()
            for edge in network.getTLSSecure(self.id).getEdges():
                for lane2 in edge._lanes:
                    if lane == lane2.getID():
                        det = 'det_' + self.id + '_' + edge.getID()
                        self.detId.append(str(det))
                        break

    def getDetectorsData(self):
        for link in range(self.linkNo):
            self.detCars[link] = traci.multientryexit.getLastStepVehicleNumber(self.detId[
                                                                               link])

    def switchLight(self):
        self.t += 1
        if self.t >= self.tmax[self.actualPhase]:
            self.getDetectorsData()
            queues = [0 for i in range(self.linkNo)]
            for link in range(self.linkNo):
                if link in self.foes[self.actualPhase]:
                    continue
                else:
                    queues[link] = self.detCars[link]
            maxQueue = queues.index(max(queues))
            # print self.id, queues
            for i in range(self.phases):
                if maxQueue in self.foes[i]:
                    newPhase = i
                    break
            self.flipTo(newPhase)
            self.tmax[newPhase] = max(queues) * self.timeCar
