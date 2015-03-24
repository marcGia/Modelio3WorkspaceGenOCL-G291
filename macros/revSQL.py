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
def basicType2UML(type):
	"""
	Convertion of SQL type into UML type
	"""
	basicTypes = theSession().getModel().getUmlTypes()
	if type == 'INT':
		return basicTypes.getINTEGER()
	elif type == 'VARCHAR':
		return basicTypes.getSTRING()
	elif type == 'BIGINT':
		return basicTypes.getLONG()
	elif type == 'SMALLINT':
		return basicTypes.getSHORT()
	elif type == 'FLOAT':
		return basicTypes.getFLOAT()
	elif type == 'DATE':
		return basicTypes.getDATE() 
	elif type == 'TEXT':
		return basicTypes.getSTRING()
	elif type == 'BOOL':
		return basicTypes.getBOOLEAN()
	else:
		return basicTypes.getUNDEFINED()
	

def generateClass(className):
	"""
	Generate a class from a table
	"""
	transaction = theSession().createTransaction('Class creation')
	try:
		factory = theUMLFactory()
		packageTarget = instanceNamed(Package,'library2uml')
		newClass = factory.createClass(className, packageTarget)
		transaction.commit()
	except:
		transaction.rollback()
		raise
		
def addAttribute(attributeName, attributeType, className):
	"""
	Add attributes to a class
	"""
	transaction = theSession().createTransaction('attribute adding')
	try:
		factory = theUMLFactory()
		classOwner = instanceNamed(Class, className)
		newAttribute = factory.createAttribute(attributeName, basicType2UML(attributeType), classOwner)
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

