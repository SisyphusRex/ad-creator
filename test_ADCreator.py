# Copyright 2025 Theodore Podewil
# GPL-3.0-or-later

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 


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
