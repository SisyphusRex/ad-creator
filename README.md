Hello! Welcome to the Active Directory Creator.

This Python program simulates the creation of a basic Active Directory.  
The program guides the user down the logical hierarchy of a network and its Active Directory, 
creating a unique Active Directory based on the user's inputs.
At the end, the created Active Directory is saved to a JSON file for the user to keep.


This project is my final submission to Harvard's CS50 Introduction to Programming with Python course taught by David J. Malan.
I chose the topic of Active Directory because I was studying computer networking at the time.
Not only did I learn valuable lessons about creating a project in Python, but I also became intimately familiar
with the back end logic of creating an Active Directory and creating a program that manages the Active Directory!

This program has some limitations: primarily in its scope and functionality.  For now, the user can only travel down
the logical hierarchy of a network and create a visual representation via JSON of the Active Directory.  Even in 
the creation, the user is limited to the number of objects he can add to the Active Directory.  This is to prevent
confusion and complexity since an Active Directory can become incredibly large.  Also, a true Active Directory
is not only the logical hierarchy of the network, but the Group Policies and Access Control Lists assigned to objects.  And in
a true Active Directory, one should be able to modify the network by moving objects around.

These limitations can be addressed by expanding the current program since the logical hierarchy is already established.  If
a better GUI is found, then the program could accept objects whose number is not predetermined.  GPOs and ACLs could be created as
their own custom classes and the original object classes have modified attributes to accept GPOs and ACLs.  More functions to determine 
the rules and consequences of having a GPO or ACL would have to be added.  Managing the Active Directory by moving objects is
much closer at hand.  One only need change an object's container and the containers', both new and old, contents to "move" an object.
This, too, must have rules that must be defined.

Thank you for your interest in this project!
If you have any questions, reach out to SisyphusRex on github.

#ADCreator requires the following pip installed modules
#1. easygui
#2. sys
#3. typing
#4. json
#5. pytest

September 26, 2024
After moving further into my studies, I realize that my classes could benefit from inheritance.  I could create an Active Directory object class and then make child classes for each type of Active Directory object (forest, tree, domain, OU, user, etc.)

Edit: 09/12/2024
I realized why I had so much trouble with my classes retaining information from previous instances.  I originally learned to program in Java, which is a Pass by Value language.  Python is a Pass by Assignment language.  Mutable objects can be mutated from within functions.  Since all of my custom classes included lists as the contents parameter, each new instance was inheriting old data.  I will have to look further into the code and see how I can rewrite it.

Edit: 10/01/2024
I discovered the correct method of initializing an instance with a mutable objects such as a list as an attribute.  
  ```python
class BeverageCollection:
  def __init__ (self, __beverages: list = None):
    """Constructor"""
    self.__beverages = __beverages or []
```
This keeps future instances from referencing the same data/memory spot as the previous instances.


_________________________________________________________________________________________

Copyright 2025 Theodore Podewil
GPL-3.0-or-later

/* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/. */
