import xml.etree.ElementTree as ET

viewsettings = ET.Element('viewsettings')
c = 0
for i in range(1,60*60*16+1,5):
	screenshot = ET.SubElement(viewsettings,"snapshot")
	screenshot.set("file","C:\\Users\\Dario\\Documents\\Proyectos\\SUMO\\src\\output\\cda\\snapshots\\snap{:05}.png".format(c))
	screenshot.set("time", str(i))
	c=c+1
xml = ET.ElementTree(viewsettings)
xml.write("cda/snapshots.xml")