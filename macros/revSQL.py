"""
=========================================================
                       revSQL.py
=========================================================

@author Giaccone Marc <marc.giaccone@laposte.net>
@author Nawaoui Swane <swane.nawaoui@gmail.com>
@group  G291

http://modelioscribes.readthedocs.org/en/latest/index.html
http://schemaspy.sourceforge.net/sample/relationships.html

Current state of the generator
----------------------------------


Current state of the tests
--------------------------


Observations
------------
Additional observations could go there
"""
import xml.etree.ElementTree as ET

pathToFile = Modelio.getInstance().getContext().getWorkspacePath().toString()+'\\library.xml'
tree = ET.parse(pathToFile)
root = tree.getroot()

for table in root.findall('tables/table'):
	print 'table '+table.get('name')+' '+table.get('numRows');
	for column in table.findall('column'):
		print'\tcolumn '+column.get('name')+' '+column.get('type')