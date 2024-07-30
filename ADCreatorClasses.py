import typing
from typing import Union

#These are the programs custom classes.  Each class is a type of Active Directory object.
#To enable moving through the Active Directory and creating a hierarchal path,
#each class (i.e. Active Directory Object), has a container and contents attribute.
#Container shows what holds the object and contents shows what the object holds.
#Since an object can only be directly in one container, container takes one argument
#An object can have many contents, so contents takes a list.

#Noticeably missing are GPOs and ACLs.  These policies are the reason for the Active Directory hierarchy and the purpose of Active Directory.
#In the future, class attributes (or new classes) such as GPO and ACL could be added to allow fore AAA control within the Active Directory
#and more realistically simulate an actual Active Directory Service.
class Forest:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents
#getters and setters were coded in for troubleshooting during development, but they are redundant for now.
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container

    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents
    
    #modify_container is a primitive "move" method.  If you change an objects container, you essentially move that object in the Active Directory
    #This method is not called in the original, basic Active Directory creation.  With some modification, it could be used to "manage" an
    #Active Directory after creation.
    def modify_container(self, n):
        self.container = n

    def add_contents(self, n: "Tree"):
        self.contents.append(n)
        

    def __str__(self):
        return f"{self.name}"

class Tree:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents
    
    def modify_container(self, n: "Forest"):
        self.container = n
    
    def add_contents(self, n: Union["Child", "Domain"]):
        self.contents.append(n)

    def __str__(self):
        return f"{self.name}"

class Child:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents
    
    def modify_container(self, n: "Tree"):
        self.container = n
    
    def add_contents(self, n: "Domain"):
        self.contents.append(n)
    
    def __str__(self):
        return f"{self.name}"

class Domain:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents

    def modify_container(self, n: Union["Tree", "Child"]):
        self.container = n
    
    def add_contents(self, n: Union["OU", "Group", "User", "Computer"]):
        self.contents.append(n)

    def __str__(self):
        return f"{self.name}"

class OU:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents
    
    def modify_container(self, n: "Domain"):
        self.container = n

    def add_contents(self, n: Union["Group", "User", "Computer"]):
        self.contents.append(n)

    def __str__(self):
        return f"{self.name}"

class Group:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents

    def modify_container(self, n: Union["OU", "Domain"]):
        self.container = n
    
    def add_contents(self, n: Union["User", "Computer"]):
        self.contents.append(n)

    def __str__(self):
        return f"{self.name}"

class User:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents

    def modify_container(self, n: Union["Group", "OU", "Domain"]):
        self.container = n

    def add_contents(self, n: None):
        self.contents.append(n)

    def __str__(self):
        return f"{self.name}"

class Computer:
    def __init__(self, name, container = None, contents = []):
        self.name = name
        self.container = container
        self.contents = contents

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def container(self):
        return self._container
    @container.setter
    def container(self, container):
        self._container = container
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self, contents):
        self._contents = contents

    def modify_container(self, n: Union["Group", "OU", "Domain"]):
        self.container = n

    def add_contents(self, n: None):
        self.contents.append(n)

    def __str__(self):
        return f"{self.name}"
