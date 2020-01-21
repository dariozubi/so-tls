import matplotlib.pyplot as plt
import numpy as np
import resultData, sys, math
sys.path.append('/usr/share/sumo/tools')
#sys.path.append('/Users/dazuma/Documents/sumo-svn/tools')
import traci

def init(dp):
  global fig, x, y, ax, line, ymax, ymax0, ylimit, dataPrint
  dataPrint = dp
  ymax0 = 5
  x = [0]
  y = [0]
  plt.ion()
  fig = plt.figure()
  ax = fig.add_subplot(111)
  line, = ax.plot(x, y, 'k-')
  ax.set_xlim([0,100])
  ymax = ymax0
  ylimit = ymax0
  plt.yticks(range(0,ymax,1))
  
def addPoints(step):
  global x, y, line, ax, ymax, ymax0, ylimit, dataPrint
  vehicles = traci.vehicle.getIDList()
  carData = resultData.datos(vehicles)
  #print carData
  x.append(step)
  y.append(carData[dataPrint])
  line.set_xdata(x)
  line.set_ydata(y)
  if step%50 == 0:
    ax.set_xlim([0,step + 50])
  if carData[dataPrint] > ymax:
    ymax = carData[dataPrint]
  if ymax > ymax0:
    if ymax > 10:
      ylimit = int(math.ceil(ymax/10.0))*10
    elif ymax > 100:
      ylimit = int(math.ceil(ymax/100.0))*100
    else:
      ylimit = ymax + 1
    ax.set_ylim([0,ylimit])
  if ylimit > 10:
    stepGraph = int(ylimit/10)
  else:
    stepGraph =  1
  plt.yticks(np.arange(stepGraph,ylimit+stepGraph,stepGraph))
  fig.canvas.draw()