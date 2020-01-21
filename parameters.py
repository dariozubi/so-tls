#!/usr/bin/env python
"""
@file    parameters.py
@author  Dario Zubillaga
@date    2014-04-1

Python parser for the different parameters of the simulation. Can be
consulted with the -h flag on the command line.

"""

import argparse

def parse():
  parser = argparse.ArgumentParser(description="Using SUMO with different trafficlight methods on a map", 
    epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  general = parser.add_argument_group('General')
  general.add_argument('-g','--gui', action='store_true', help='Use sumo-gui')
  general.add_argument('-n','--dirNet', default='cda', help='File directory with the network files')
  output = parser.add_argument_group('Output')
  output.add_argument('-s','--dataNum', type=int, default=0, help='File number to be printed')
  tls = parser.add_argument_group('Traffic lights')
  tls.add_argument('-t','--tls', type=int, default=1, choices=[0,1,2,3],
    help='Trafficlight type: fixed(0), self-organized(1), proportional to previous cycles(2), queue(3)')
  tls.add_argument('--tlsPrograms', default='TLSprograms.txt', help='File with the TLS programs description')
  sotl = parser.add_argument_group('Self-organized traffic lights')
  sotl.add_argument('--treshold', type=int, default=13, help='Treshold for the SO method')
  sotl.add_argument('--miniTreshold', type=int, default=1, help='miniTreshold for the SO method')
  sotl.add_argument('--phaseMin', type=int, default=13, help='Minimum phase for the SO method')
  cycles = parser.add_argument_group('Proportional to previous cycles traffic lights')
  cycles.add_argument('--cycles', type=int, default=10, help='Number of previous cycles')
  parameters = parser.parse_args()
  names = {0:'fixed',1:'self-organized',2:'proportional to previous cycles',3:'maximum queue'}
  print '\n  Parameters:'
  print '\t tls: {0}'.format(names[parameters.tls])
  print '\t dirNet: {0}'.format(parameters.dirNet)
  print '\t dataNum: {0}'.format(parameters.dataNum)
  print '\t tlsPrograms: {0} \n'.format(parameters.tlsPrograms)
  return parameters
