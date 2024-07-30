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