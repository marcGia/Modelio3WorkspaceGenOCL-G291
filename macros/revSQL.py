"""
=========================================================
                       revSQL.py
=========================================================

@author Giaccone Marc <marc.giaccone@laposte.net>
@author Nawaoui Swane <swane.nawaoui@gmail.com>
@group  G291

http://modelioscribes.readthedocs.org/en/latest/index.html

Current state of the generator
----------------------------------


Current state of the tests
--------------------------


Observations
------------
Additional observations could go there
"""
import xml.etree.ElementTree as ET

#---------------------------------------------------------
#          			XML Reading functions
#---------------------------------------------------------
# These functions allow to read the xml file 
#---------------------------------------------------------
pathToFile = Modelio.getInstance().getContext().getWorkspacePath().toString()+'\\library.xml'
tree = ET.parse(pathToFile)
root = tree.getroot()

def readColumns(table):
	"""
	Return the list of columns in a table
	"""
	columnsList = []
	for column in table.findall('column'):
		columnsList.append(column)
	return columnsList

def readTables():
	"""
	Return the list of tables from the xml
	"""
	tablesList = []
	for table in root.findall('tables/table'):
		tablesList.append(table)
	return tablesList
		
#---------------------------------------------------------
#       		UML Generation functions
#---------------------------------------------------------
# These functions allow to generate UML from xml 
#---------------------------------------------------------
transaction = theSession().createTransaction("Class creation")
try:
  factory = theUMLFactory()
  packageTarget = instanceNamed(Package,"library2uml")
  class1 = factory.createClass("Voiture", packageTarget)
  class2 = factory.createClass("Roue",packageTarget)
  transaction.commit()
except:
  transaction.rollback()
  raise


#---------------------------------------------------------
#       				Main
#---------------------------------------------------------
for table in readTables():
	print 'table '+table.get('name')+' '+table.get('numRows');
	for column in readColumns(table):
		print'\tcolumn '+column.get('name')+' '+column.get('type')

