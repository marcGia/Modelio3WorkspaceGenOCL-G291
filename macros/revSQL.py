"""
=========================================================
                       revSQL.py
=========================================================

@author Giaccone Marc <marc.giaccone@laposte.net>
@author Nawaoui Swane <swane.nawaoui@gmail.com>
@group  G291

# Documentation:
# for transactions: http://forge.modelio.org/projects/modelio3-moduledevelopersmanuals-api/wiki/Transaction_api
# for the uml factory: http://modelio.org/documentation/javadoc-3.1/org/modelio/api/model/IUmlModel.html
# for example: http://modelioscribes.readthedocs.org/en/latest/index.html
# for library relational model: http://schemaspy.sourceforge.net/sample/relationships.html

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
	for column in table.findall('column'):
		print'\tcolumn '+column.get('name')+' '+column.get('type')

def readTables():
	for table in root.findall('tables/table'):
		print 'table '+table.get('name')+' '+table.get('numRows');
		readColumns(table)
		
		
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
readTables()

