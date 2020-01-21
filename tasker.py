import winsound,subprocess, datetime

times = ""
for i in range(20,220,20):
  print("##################################################################\n##################################################################\n######################                      ######################\n######################        DEC           ######################\n######################        {:03}%          ######################\n######################                      ######################\n##################################################################\n##################################################################\n".format(i))
  times = times + str(i) +"%:"+str(datetime.datetime.now())[11:19]
  # cmd = 'copy /y input\\cda\\flows_february\\cda.rou-{0}.xml input\\cda\\cda.rou.xml'.format(i)
  # subprocess.call(cmd,shell=True)
  # cmd = 'python runner.py -s {0}'.format(i)
  # subprocess.call(cmd,shell=True)
  # times = times + " - Selforg: " + str(datetime.datetime.now())[11:19]
  # cmd = 'ping 127.0.0.1 -n 16 > nul'
  # subprocess.call(cmd,shell=True)
  # cmd = 'python runner.py -t 0 -s {0}'.format(i)
  # subprocess.call(cmd,shell=True)
  # times = times + " - Fixed: " + str(datetime.datetime.now())[11:19]
  # cmd = 'ping 127.0.0.1 -n 16 > nul'
  # subprocess.call(cmd,shell=True)
  cmd = 'python output\\parseResults.py -n cda -s {0}'.format(i)
  subprocess.call(cmd,shell=True)
  times = times + " - " + str(datetime.datetime.now())[11:19] + "\n"
  print(times)

winsound.MessageBeep()
cmd = 'ping 127.0.0.1 -n 2 > nul'
subprocess.call(cmd,shell=True)
winsound.MessageBeep()
cmd = 'ping 127.0.0.1 -n 2 > nul'
subprocess.call(cmd,shell=True)
winsound.MessageBeep()


