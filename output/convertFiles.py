import sys, random, subprocess, os, argparse, math
sys.path.append('/usr/share/sumo/tools')
import sumolib.net

def parse():
  parser = argparse.ArgumentParser(description="Convert xml data to csv using the xml2csv tool from SUMO", 
    epilog="Dario Zubillaga 2014", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  general = parser.add_argument_group('General')
  general.add_argument('-n','--name', help='Directory name', required=True)
  general.add_argument('-f','--files', type=int,help='Number of files', required=True)
  parameters = parser.parse_args()
  return parameters
  
par = parse()

for i in range(par.files):
  subprocess.call('python xml2csv.py {1}/summary_fixed_{0}.xml'.format(i,par.name), shell=True)
  subprocess.call('sed -i "1d" {1}/summary_fixed_{0}.csv'.format(i,par.name), shell=True)
  subprocess.call('python xml2csv.py {1}/summary_prevcycles_{0}.xml'.format(i,par.name), shell=True)
  subprocess.call('sed -i "1d" {1}/summary_prevcycles_{0}.csv'.format(i,par.name), shell=True)
  subprocess.call('python xml2csv.py {1}/summary_queue_{0}.xml'.format(i,par.name), shell=True)
  subprocess.call('sed -i "1d" {1}/summary_queue_{0}.csv'.format(i,par.name), shell=True)
  subprocess.call('python xml2csv.py {1}/summary_sotl_{0}.xml'.format(i,par.name), shell=True)
  subprocess.call('sed -i "1d" {1}/summary_sotl_{0}.csv'.format(i,par.name), shell=True)