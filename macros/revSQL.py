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
	"""
	Return the list of columns in a table
	"""
	columnsList = []
	for column in table.findall('column'):
		columnsList.append(column)
	return columnsList

class ColumnInfo:
	kind = ''
	type = ''
	className = ''
	attributeName = ''
	source = ''
	target = ''
	
def readColumnInfo(column):
	"""
	Return informations about the column passed in parameter
	"""
	columnType = column.find('parent')
	
	className = table.get('name')
	columnInfo = ColumnInfo()
	columnInfo.type = column.get('type')
	if columnType is None:
		# 'columnType' is an attribute
		attributeName = column.get('name')

		# --> Build attribute
		# level 1: all entries are simple attributes
		print '\tCreate level1 attribute: '+attributeName+' in '+className
		columnInfo.kind = 'attribute'
		columnInfo.className = className
		columnInfo.attributeName = attributeName

	else:
		# 'columnType' is a foreign key hence represented by an association
		source = columnType.get('column')
		
		referencedClass = columnType.get('table')
		referencedClass_column = columnType.get('foreignKey')
		
		ref = root.find("tables/table[@name='"+referencedClass+"']")
		
		# find the column with the right foreign key
		ref_column = ref.find("column/child[@foreignKey='"+referencedClass_column+"']/..")
		
		destination = ref_column.get('name')

		# --> Build association
		print '\tCreate level1 association: '+className+' <--> '+referencedClass
		print '\tCreate level2 association: '+className+' --> '+referencedClass
		print '\tCreate level3 association: '+className+'.'+source+' --> '+referencedClass+"."+destination

		columnInfo.kind = 'association'
		columnInfo.source = className
		columnInfo.target = referencedClass
		
	return columnInfo

def readTables():
	"""
	Return the list of tables from the xml
	"""
	tablesList = []
	for table in root.findall('tables/table'):
		className = table.get('name')
		tablesList.append(table)

		# --> Build class
		print 'Create class '+className

		readColumns(table)
		
	return tablesList

#---------------------------------------------------------
#       		UML Generation functions
#---------------------------------------------------------
# These functions allow to generate UML from xml 
#---------------------------------------------------------
def cleanPackage(packageName):
	"""
	Delete all elements in the package packageName(String)
	"""
	transaction = theSession().createTransaction('clean package')
	try:
		packageTarget = instanceNamed(Package, packageName)
		elements = list(packageTarget.getOwnedElement())

		for element in elements:
			element.delete()
			
		transaction.commit()
	except:
		transaction.rollback()
		raise

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

def generateClass(className, packageName):
	"""
	Generate a class with the name className(String) with the "T" stereotype
	"""
	transaction = theSession().createTransaction('Class creation')
	try:
		factory = theUMLFactory()
		packageTarget = instanceNamed(Package, packageName)
		newClass = factory.createClass(className, packageTarget)
		newClass.addStereotype("LocalModule", "T")
		transaction.commit()
	except:
		transaction.rollback()
		raise
		
def addAttribute(attributeName, attributeType, className):
	"""
	Add the attributes attributeName(String) with attributeType(UMLType) to the class className(String)
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
		
def addAssociation(srcClassName, destClassName, destRole):
	"""
	Create the association from the class srcClassName(String) to the destClassName(String) with the given 
	destination role destRole(String) and with the "FKC" stereotype
	"""
	transaction = theSession().createTransaction('association adding')
	try:
		factory = theUMLFactory()
		src = instanceNamed(Class, srcClassName)
		dest = instanceNamed(Class, destClassName)
		newAssociation = factory.createAssociation(src, dest, destRole)
		newAssociation.addStereotype("LocalModule", "FKC")
		transaction.commit()
	except:
		transaction.rollback()
		raise

#---------------------------------------------------------
#       				Main
#---------------------------------------------------------
for element in selectedElements:
	if isinstance(element, Package):
		packageName = element.getName()
		cleanPackage(packageName)
		
		# Creation of classes and attributes
		for table in readTables():
			generateClass(table.get('name'), packageName)
			for column in readColumns(table):
				columnInfo = readColumnInfo(column)
				if columnInfo.kind == 'attribute':
					addAttribute(columnInfo.attributeName, columnInfo.type, table.get('name'))
		
		# Creation of relations
		for table in readTables():
			for column in readColumns(table):
				columnInfo = readColumnInfo(column)
				if columnInfo.kind == 'association':
					addAssociation(columnInfo.source, columnInfo.target, columnInfo.target+'s')
