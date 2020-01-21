import xml.etree.ElementTree as ET
import math
import sys
import subprocess
import os
from datetime import date, time, datetime, timedelta

def speedLarge():
    vehiclesFile = 'cda/vehicles.xml'
    context = ET.iterparse(vehiclesFile, events=('start', 'end'))
    context = iter(context)
    event, root = context.next()
    totalLength = 0
    c = 0
    p = 0
    # totalVehicleFile = open('cda/vehicles_selforg_100_dic.csv', 'a')
    # d = date(2017,12,20)
    # t = time(6,0)
    # start = datetime.combine(d,t)
    # ref = datetime.combine(d,t)
    # d = date(2017,12,20)
    # t = time(22,1)
    # end = datetime.combine(d,t)
    for event, elem in context:
        if event == "end" and elem.tag == "timestep":
            vehicleNumber = 0
            for vehicle in elem.iter('vehicle'):
                vehicleFile = open('cda/vehicles/vehicle{}.txt'.format(vehicle.get("id").replace(".","-")), 'a')
                line = '{},{},{},{}\n'.format(c,vehicle.get('lat'),vehicle.get('lon'),vehicle.get('speed'))
                vehicleFile.write(line)
                vehicleFile.close()
            # if (start == ref):
            #     print(str(ref))
            #     ref = ref + (timedelta(hours=1))
            # start = start + timedelta(seconds=10)
            if (c%76 == 1):
                print(str(p)+"%")
                p = p + 5
            c=c+1

            root.clear()
    # totalVehicleFile.close()

speedLarge()
