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
		columnType = column.find('parent')

		className = table.get('name')
		if columnType is None:
			# 'columnType' is an attribute
			attributeName = column.get('name')

			# --> Build attribute
			print '\tCreate attribute '+attributeName+' in '+className
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

		columnsList.append(column)
	return columnsList

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

def generateClass(className):
	"""
	Generate a class with the name className(String)
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
	destination role destRole(String)
	"""
	transaction = theSession().createTransaction('association adding')
	try:
		factory = theUMLFactory()
		src = instanceNamed(Class, srcClassName)
		dest = instanceNamed(Class, destClassName)
		newAssociation = factory.createAssociation(src, dest, destRole)
		transaction.commit()
	except:
		transaction.rollback()
		raise

#---------------------------------------------------------
#       				Main
#---------------------------------------------------------
cleanPackage('library2uml')

for table in readTables():
	#print 'table '+table.get('name')+' '+table.get('numRows');
	generateClass(table.get('name'))
	for column in readColumns(table):
		#print'\tcolumn '+column.get('name')+' '+column.get('type')
		addAttribute(column.get('name'), column.get('type'), table.get('name'))

