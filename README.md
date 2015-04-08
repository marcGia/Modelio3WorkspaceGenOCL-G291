
Modelio3WorkspaceGenOCL-G291 (Giaccone Marc & Nawaoui Swane)
===========================

Summary
------------
This repository contains an OCL generator from UML schema and a modelio 
generator from xml file representing an SQL database.

OCL generator
---------------
Thanks to this generator, don't lose time anymore with the creation 
of the schema in OCL, it does it for you. You can directly focus on
the constraint creation and test.

* **How to use ?**
   1. Create a modelio project
   2. In a package, create your UML schema
   3. When your schema's done, click you package containing your schema and
      click the 'GenOCL' macro
   4. Copy the OCL result from the console output
Enumerations are created after classes, so when you copy-paste the OCL 
result, you have to first copy-paste the enumerations creation and then 
the classes creation (because classes can use enumerations).

* **Current features**
The generator is currently able to generate :
   + classes
   + attributes with cardinalities
   + enumerations
   + operations
   + inheritance (simple and multiple)
   + simple associations (can be unspecified or ordered)
   + compositions
   + aggregations
   + association classes

* **Missing features**
The generator is currently NOT able to generate :
   + associations qualified
   + associations NAry
   + notes

* **Issues**
   no issue detected at the moment

* **Tests**
Each feature of the generator has been tested on single and precise examples.
Then the generator has been tested with a real example.
You can find more informations about tests in the GenOCL file.

Modelio Generator 
-----------------------------------------------
Thanks to this generator, you can quickly have an UML representation of 
your sql database.

* **How to use ?**
   1. Create a modelio project
   2. In this project, create a new package
   3. Add a new profile with 4 stereotypes: 'T'(for class), 'PK'(for attribute), 
       'FK'(for attribute) and 'FKC'(for dependency).
   3. Place your xml file named 'library.xml' in your modelio workspace
   4. Select the package you created and click the 'revSQL' macro.
You execute the macro more than once, the system clean the package selected before
each execution.

* **Current features**
The generator is currently able to represent :
   + tables with classes which have a 'T' stereotype
   + columns with attributes
   + primary keys by adding a 'PK' stereotype to attributes
   + foreign keys by adding a 'FK' stereotype to attributes
   + relations with dependencies between a 'PK' attribute and a 'FK' attribute
      of two different classes. The dependency has the 'FKC' stereotype

* **Missing features**
The generator is currently NOT able to generate :
   + Create the schema representation

* **Issues**
   no issue detected at the moment

* **Tests**
The generator has been tested with a real example and results have been verified
with a reference schema.
You can find more informations about tests in the GenOCL file.
