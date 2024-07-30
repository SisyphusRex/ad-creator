import pytest
from ADCreatorMain import *
from ADCreatorClasses import *
from ADCreatorFunctions import *

def test_1():
    assert check_OU_group_user_computer_input("Bob")

def test_2():
    my_forest = Forest("steve", container = None, contents = [])
    my_tree = Tree("bob", container = None, contents = [])
    assert my_forest.name == "steve"
    assert my_forest.container == None
    assert my_forest.contents == []
    my_tree.modify_container(my_forest)
    my_forest.add_contents(my_tree)
    assert my_tree.container == my_forest
    assert my_tree in my_forest.contents

def test_3():
    assert check_forest_input("hardware.com")
