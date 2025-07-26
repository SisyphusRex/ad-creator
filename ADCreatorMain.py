# Copyright 2025 Theodore Podewil
# GPL-3.0-or-later

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 


from ADCreatorClasses import *
from easygui import *
from ADCreatorFunctions import *
import json

#This is the main file and program.  intro() constructs the Active Directory through GUI prompts
#create_new_dict prepares a dictionary of the Active Directory that is then written to a JSON file for viewing.
#goodbye() just says goodbye
def main():
    user_forests = intro()
    my_dict = create_new_dict(user_forests)
    with open("test.json", "w") as my_file:
        json.dump(my_dict, my_file, indent = 4)
    goodbye()
    
    
if __name__ == "__main__":
    main()
