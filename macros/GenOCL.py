"""
=========================================================
                       GenOCL.py
 Generate a USE OCL specification from a UML package
=========================================================

FILL THIS SECTION AS SHOWN BELOW AND LINES STARTING WITH ###
@author Giaccone Marc <marc.giaccone@laposte.net>
@author Nawaoui Swane <swane.nawaoui@gmail.com>
@group  G291

Current state of the generator
----------------------------------
Etat actuel:
- classes 					-> OK
- attributes simple 		-> OK
- attributes visibility		-> OK
- attributes cardinality	-> OK
- attributes enumarations	-> OK
- operations				-> OK
- inheritance simple		-> OK
- inheritance multiple		-> OK
- associations simple		-> OK
- associations unspecified	-> OK
- associations ordered		-> OK
- associations composition	-> OK
- associations aggregation	-> OK
- associations class		-> OK
- associations qualified	-> TODO
- associations NAry			-> TODO
- notes 					-> TODO

limitations:
L'ordre n'est pas toujours respecté. Par exemple les enumerations sont crees après les classes, ce qui
est problematique si la classe possède un attribut du type de cette enumeration. Il faut donc copier-coller
la sortie générée dans le bon ordre pour USE OCL.

Current state of the tests
--------------------------
- Le script GenOCL est exécuté sur chaque package du projet UMLTestCase durant le developpement d'une 
fonctionnalité jusqu'à ce que l'affichage nous paraisse correct.

- L'affichage générée par les script GenOcl est testé avec le programme de USE (copié-coller de la sortie). Si 
aucune erreurs n'est annoncé et que le schéma UML affiché par le programme USE correspond à celui du projet 
UMLTestCase alors le test est validé.

- Une fonctionnalité est developpée jusqu'à ce que les tests soit validés.

Observations
------------
Additional observations could go there
"""


#---------------------------------------------------------
#   Helpers on the source metamodel (UML metamodel)
#---------------------------------------------------------
# The functions below can be seen as extensions of the
# modelio metamodel. They define useful elements that 
# are missing in the current metamodel but that allow to
# explorer the UML metamodel with ease.
# These functions are independent from the particular 
# problem at hand and could be reused in other 
# transformations taken UML models as input.
#---------------------------------------------------------

# example
def isAssociationClass(element):
    """ 
    Return True if and only if the element is an association 
    that have an associated class, or if this is a class that
    has a associated association. (see the Modelio metamodel
    for details)
    """
    return len(element.getTargetingEnd())!=0
    
 
#---------------------------------------------------------
#   Application dependent helpers on the source metamodel
#---------------------------------------------------------
# The functions below are defined on the UML metamodel
# but they are defined in the context of the transformation
# from UML Class diagramm to USE OCL. There are not
# intended to be reusable. 
#--------------------------------------------------------- 

# example
def associationsInPackage(package):
	"""
	Return the list of all associations that start or
	arrive to a class which is recursively contained in
	a package.
	"""
	associationList = []
	for element in package.getOwnedElement():
		if isinstance(element, Class):
			for associationEnd in element.getOwnedEnd():
				association = associationEnd.getAssociation()
				if association not in associationList:
					associationList.append(association)
	
	return associationList

    
#---------------------------------------------------------
#   Helpers for the target representation (text)
#---------------------------------------------------------
# The functions below aims to simplify the production of
# textual languages. They are independent from the 
# problem at hand and could be reused in other 
# transformation generating text as output.
#---------------------------------------------------------


# for instance a function to indent a multi line string if
# needed, or to wrap long lines after 80 characters, etc.

#---------------------------------------------------------
#           Transformation functions: UML2OCL
#---------------------------------------------------------
# The functions below transform each element of the
# UML metamodel into relevant elements in the OCL language.
# This is the core of the transformation. These functions
# are based on the helpers defined before. They can use
# print statement to produce the output sequentially.
# Another alternative is to produce the output in a
# string and output the result at the end.
#---------------------------------------------------------



# examples

def umlEnumeration2OCL(enumeration):
	"""
	Generate USE OCL code for the enumeration
	"""
	print 'enum '+enumeration.getName()+' {'
	
	enumLen = len(enumeration.getValue())
	for index, enum in enumerate(enumeration.getValue()):
		if index < enumLen-1:
			print indent(2)+enum.getName()+','
		else:
			print indent(2)+enum.getName()
	
	print '}'

	
def umlBasicType2OCL(basicType):
	"""
	Generate USE OCL basic type. Note that
	type conversions are required.
	"""
	typeName = basicType.getName()
	
	if isinstance(basicType, Class) or isinstance(basicType, Enumeration):
		return typeName
	elif typeName == 'float':
		return 'Real'
	else:
		return typeName.capitalize()
	
	
def umlMultiplicity2OCL(min, max):
	"""
	Generate USE OCL Multiplicity
	"""
	if min != max and (min!='0' or max!='*'):
		return ' ['+min+'..'+max+'] '
	else:
		return ' ['+max+'] '
	
def umlKindOfAssociation2OCL(associationKind):
	"""
	Determine the type of the association
	"""
	if associationKind == 'KindIsComposition':
		return 'composition'
	elif associationKind == 'KindIsAggregation':
		return 'aggregation'
	else:
		return 'association'
	

def association2OCL(association):
	"""
	Generate USE OCL association
	"""
	associationType = 'association'
	associationContent = ''
	
	# Les classes associatives sont gerees dans class2OCL
	if(not association.getLinkToClass()):
		for associationEnd in association.getEnd():
			if(associationEnd.getName() != ''):
				role = 'role '+associationEnd.getOpposite().getName()
			else:
				role = ''
			# Si c'est une composition ou une aggregation, une des associationEnd est de type composition ou aggregation
			# Si c'est une composition ou une aggregation, l'entree courante doit etre place au debut du contenu de la composition
			type = umlKindOfAssociation2OCL(str(associationEnd.getAggregation()))
			if type == 'composition' or type == 'aggregation':
				associationType = type
				associationContent = indent(2)+associationEnd.getOwner().getName()+umlMultiplicity2OCL(associationEnd.getOpposite().getMultiplicityMin(), associationEnd.getOpposite().getMultiplicityMax())+role+'\n'+associationContent
			else:
				associationContent += indent(2)+associationEnd.getOwner().getName()+umlMultiplicity2OCL(associationEnd.getOpposite().getMultiplicityMin(), associationEnd.getOpposite().getMultiplicityMax())+role+'\n'
		print associationType+' '+association.getName()+' between'
		print associationContent+'end\n'
		
def operation2OCL(operation):
	"""
	Generate USE OCL operations
	"""
	parameters = ''
	if len(operation.getIO())>0:
		for index, parameter in enumerate(operation.getIO()):
			parameters += parameter.getName()+': '+umlBasicType2OCL(parameter.getType())
			if index < len(operation.getIO())-1:
				parameters += ', '
	
	returnedType = '' if operation.getReturn() is None else ': '+umlBasicType2OCL(operation.getReturn().getType())
	
	return operation.getName()+'('+parameters+') '+returnedType
	
	
def umlClass2OCL(classe):
	"""
	Generate USE OCL classes
	"""
	abstract = 'abstract ' if classe.isIsAbstract() else ''
	
	linkAssociation = classe.getLinkToAssociation()
	if(linkAssociation):
		classType = 'associationclass '
		blocAssociation = 'between\n'
		for associationEnd in linkAssociation.getAssociationPart().getEnd():
			if(associationEnd.getName() != ''):
				role = 'role '+associationEnd.getName()
			else:
				role = ''
			blocAssociation = blocAssociation+indent(2)+associationEnd.getOwner().getName()+umlMultiplicity2OCL(associationEnd.getMultiplicityMin(), associationEnd.getMultiplicityMax())+role+'\n'
	else:
		classType = 'class '
		blocAssociation = ''
		
	parents = classe.getParent()
	if(parents):
		superClasses = ' < '
		for i in range(len(parents)):
			if(i == 0):
				superClasses = superClasses + parents[0].getSuperType().getName()
			else:
				superClasses = superClasses + ', '+parents[i].getSuperType().getName()

		print abstract+classType+classe.getName()+superClasses
	else:
		print abstract+classType+classe.getName()
	
	# Ecriture des association (si elles existent)
	if(blocAssociation != ''):
		print blocAssociation
	
	# Ecriture des attributs
	if len(classe.getOwnedAttribute())>0:
		print 'attributes'
		for attribute in classe.getOwnedAttribute():
			derived = '  -- @derived' if attribute.isIsDerived() else ''
			print indent(2)+attribute.getName()+' : '+umlBasicType2OCL(attribute.getType())+derived
	
	# Ecriture des methodes (si elles existent)
	operations = classe.getOwnedOperation()
	if len(operations) > 0:
		print 'operations'
		for operation in operations:
			print indent(2)+operation2OCL(operation)
	
	print 'end\n'
	
	
def package2OCL(package):
    """
    Generate a complete OCL specification for a given package.
    The inner package structure is ignored. That is, all
    elements useful for USE OCL (enumerations, classes, 
    associationClasses, associations and invariants) are looked
    recursively in the given package and output in the OCL
    specification. The possibly nested package structure that
    might exist is not reflected in the USE OCL specification
    as USE is not supporting the concept of package.
    """
    for element in package.getOwnedElement():
	  if isinstance(element, Class):
	    umlClass2OCL(element)
	  elif isinstance(element, Enumeration):
	    umlEnumeration2OCL(element)
	  elif isinstance(element, Package):
	    package2OCL(element)
	  
    for association in associationsInPackage(package):
		association2OCL(association)


#---------------------------------------------------------
#           User interface for the Transformation 
#---------------------------------------------------------
# The code below makes the link between the parameter(s)
# provided by the user or the environment and the 
# transformation functions above.
# It also produces the end result of the transformation.
# For instance the output can be written in a file or
# printed on the console.
#---------------------------------------------------------

# (1) computation of the 'package' parameter
# (2) call of package2OCL(package)
# (3) do something with the result
for element in selectedElements:
	if isinstance(element, Package):
		print 'model '+element.getName()+'\n'
		package2OCL(element)
	else:
		print 'Selectionnez un package!'
