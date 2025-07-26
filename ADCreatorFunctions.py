# Copyright 2025 Theodore Podewil
# GPL-3.0-or-later

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 


from easygui import *
from ADCreatorClasses import *
import sys

#This is the engine of the Active Directory Creator.  The ADCreatorMain file calls intro() and all of the work takes place here, behind the scenes.

#Says Hello
def intro():
    x_button_check(msgbox("Welcom to Active Directory Builder!\n\nClick OK to continue."))
    x_button_check(msgbox("Let us create the forest."))
    user_forest = create_user_forest()
    #the final output of intro() is user_forest.  This is is an instance of the ADCreatorClasses class Forest.  It contains the entire Active Directory. 
    return user_forest
#The functions to create each level are nested within eachother.  
#To create a Forest, you must create a Tree or Trees
#To create a Tree, you must create Children
#To create Children, you must create Domains
#and so forth until you reach the last object in a branch.

#each function returns a list of objects created.  Since an Active Directory can have many objects at each level, 
#returning a list allows for an undetermined number of objects to be returned.
def create_user_forest() -> list:
    #when troubleshooting a problem with inherited attributes, I went to each function and instantiated the problem object to none or empty set
    #they were not the cause of the inheritance issue but helped me narrow it down.
    my_forests = None
    my_forests = []
    good_answer = False
    while good_answer == False:
        #This program only accepts Top Level domain names.
        answer = x_button_check(enterbox("What is the name of your forest root domain?\n"
                                      "Only top level domain names will be accepted:\n"
                                      ".com, .org, .net, .int, .edu, .gov, .mil"
                                      "\n\nBy convention, this will also be the name of your forest.\n"
                                      "Example: hardware.com", "Create Forest"))
        #checks for correct format of User input
        good_answer = check_forest_input(answer)
    #here we create our first object and add it to a list.  While most Active Directories can have multiple forests, it is discouraged
    #and not allowed in this program.  Although, my_forests is a list and can contain more than one forest
    my_forests.append(Forest(answer, None, contents = []))
    x_button_check(msgbox(f"The name of your forest is {my_forests[0]}"))
    #here we iterate over all of the forests created (only one for our purposes, but iteration allows for more than one)
    #and populate the forest with trees.
    for forest in my_forests:
        tree_list = None
        tree_list = create_user_tree(forest)
        for tree in tree_list:
            #We use a class method to update our forest object after the tree(s) are created
            forest.add_contents(tree)
    return my_forests
    

def create_user_tree(forest) -> list:
    my_trees = None
    my_trees = []
    #The container_list is a way for the user to see where he is working in the Active Directory.  Since I am using a simple GUI,
    #the user can become lost quickly.  I have limited the number of objects that can be created at each level
    #and I display the current Active Directory path to help the user orient himself
    container_list = format_container_list(forest)
    #Get the number of trees.  I use a button box to limit the input of the user.  An Active Directory can grow unwieldly fast.
    tree_count_message = x_button_check(buttonbox(f"Current Location:\n{container_list}\n\nHow many Trees are in the {forest} Forest?\n\nHint:\nEach Tree is a collection "
                                   "of one or more domains with contiguous domain names.\n"
                                   "Example:\nhardware.com, sales.hardware.com, and us.sales.hardware.com are "
                                   "all of the same Tree, hardware.com.", f"Create Trees for {forest}",
                                   ("1 Tree", "2 Trees")))
    tree_count = int((tree_count_message.split())[0])
    #in AD, the forest root domain is the first tree
    x_button_check(msgbox("The first tree will by default be your forest root domain.\n\n"
           f"{forest} is your first tree."))
    #create the Tree object
    my_trees.append(Tree(forest.name, forest, contents = []))
    for tree in range(1, tree_count):
        good_answer = False
        while good_answer == False:
            answer = x_button_check(enterbox(f"Current Location:\n{container_list}\n\nWhat is the name of Tree number {tree + 1}?"))
            good_answer = check_forest_input(answer)
        #create the Tree objects after the first Tree.  This is where I solved the inherited attribute issue.
        #The name and container are instantiated but I originally left the contents attribute blank.
        #Future objects kept inheriting previous objects contents, so I instantiated the contents to empty set
        #each time I created an object.
        my_trees.append(Tree(answer, forest, contents = []))
        x_button_check(msgbox(f"Current Location:\n{container_list}\n\nThe name of your second Tree is {my_trees[1]}"))
    #Now we check if the tree has any contents and add them if necessary using the .add_contents method
    for tree in my_trees:   
        child_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes Tree {tree} have any Child/subdomains?\n\nExample: pc.hardware.com and "
                               "mac.hardware.com are Children of hardware.com", f"Create Children for {tree}"))
        if child_response:
            child_list = None
            child_list = create_user_child(tree)
            for child in child_list:
                tree.add_contents(child)
        else:
            x_button_check(msgbox(f"Current Location:\n{container_list}\n\nSince the Tree {tree} has no Children or subdomains, {tree} will be the final domain name.\n\n"
                   "Let's organize the domain now.", f"Organize Domain for {tree}"))
            domain_list = None
            domain_list = create_user_domain(tree)
            for domain in domain_list:
                tree.add_contents(domain)
    return my_trees
    
#create child objects
def create_user_child(tree) -> list:
    #to prevent an unwieldly AD, I limit the levels of subdomains.  With a better GUI, this program could handle more
    x_button_check(msgbox(f"This program can only work with one level of Children or subdomains.\n\nFor Example:\nNormally, the subdomain "
               "pc.hardware.com can be broken down further into sales.pc.hardware.com and hr.pc.hardware.com\n"))
    my_childs = None
    my_childs = []
    container_list = format_container_list(tree)
    child_count_message = x_button_check(buttonbox(f"Current Location:\n{container_list}\n\nHow many Children are in the {tree} tree?\n\nExample: pc.hardware.com "
                                    "and mac.hardware.com are the 2 Children, or subdomains, of hardware.com", f"Create Children for {tree}",
                                   ("1 Child", "2 Children")))
    child_count = int((child_count_message.split())[0])
    for child in range(child_count):
        good_answer = False
        while good_answer == False:
            answer = x_button_check(enterbox(f"Current Location:\n{container_list}\n\nWhat is the name of Child number {child + 1}\n\nExample: "
                                        "pc.hardware.com is the name of hardware.com's first Child.\n"
                                        "mac.hardware.com is the name of hardware.com's second Child", f"Name Child #{child + 1} for {tree}"))
            good_answer = check_child_input(answer, tree)
        my_childs.append(Child(answer, tree, contents = []))
        x_button_check(msgbox(f"Current Location:\n{container_list}\n\nChild #{child + 1} for Tree {tree} is {my_childs[child]}"))
    for child in my_childs:
        domain_list = None
        x_button_check(msgbox(f"Current Location:\n{container_list}\n\nWe will not divide the domain name further here.\n\n{child} will be the final domain name."))
        domain_list = create_user_domain(child)
        for domain in domain_list:
            child.add_contents(domain)
    return my_childs
    
#Creating Domains seems redundant since they inherit the name of their container
#but domains are essential to Active Directory
#Each domain contains its own Domain Controller and is managed at the domain level
def create_user_domain(n: Union["Tree", "Child"]) -> list:
    my_domains = None
    my_domains = []
    container_list = format_container_list(n)
    my_domains.append(Domain(n.name, n, contents = []))
    #a domain can contain 4 types of objects: OUs, Groups, Users, and Computers.  We must ask about each object
    for domain in my_domains:
        ou_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes {domain} contain any Organizational Units?\n\n"
                            "Hint:\n"
                            "OUs are logical containers within an Active Directory Domain.", f"Create OUs for {domain}"))
        if ou_response:
            ou_list = None
            ou_list = create_user_ou(domain)
            for ou in ou_list:
                domain.add_contents(ou)
        group_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes the Domain {domain} contain any Groups directly?\n\n"
                                "Hint:\n"
                                "Groups are containers of Active Directory objects, such as\n"
                                "Users, Computers, etc.", f"Create Groups for {domain}"))
        if group_response:
            group_list = None
            group_list = create_user_group(domain)
            for group in group_list:
                domain.add_contents(group)

        user_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes Domain {domain} contain any Users directly?\n"
                                             "(these users are not in an OU or Group)\n\n"
                                "Hint:\n"
                                "Users are actual people in the network.", f"Create Users for {domain}"))
        if user_response:
            user_list = None
            user_list = create_user_user(domain)
            for user in user_list:
                domain.add_contents(user)
        computer_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes Domain {domain} contain any computers?\n"
                                                 "(these computers are not in an OU or Group)"
                                    "Hint\n"
                                        "Computers can be any network device such as desktops or printers\n"
                                        "or servers.", f"Create Computers for {domain}"))
        if computer_response:
            computer_list = None
            computer_list = create_user_computer(domain)
            for computer in computer_list:
                domain.add_contents(computer)
    return my_domains
#create Organizational Units, essential to applying Group Policy within a domain
def create_user_ou(domain: "Domain") -> list:
    x_button_check(msgbox(f"This program can only work with one level of Organizational Units.\n\nNormally, "
               "you could add OUs to another OU to further divide the original Organizational Unit."))
    my_ous = None
    my_ous= []
    container_list = format_container_list(domain)
    ou_count_message = x_button_check(buttonbox(f"Current Location:\n{container_list}\n\nHow many Organizational Units are in the '{domain}' Domain?\n\nExample:\nUsers "
                                    "and Computers are typical OUs for a domain.", f"Create Organizational Units for {domain}",
                                   ("1 OU", "2 OU")))
    ou_count = int((ou_count_message.split())[0])
    for ou in range(ou_count):
        good_answer = False
        while good_answer == False:
            answer = x_button_check(enterbox(f"Current Location:\n{container_list}\n\nWhat is the name of OU number {ou + 1}"))
            good_answer = check_OU_group_user_computer_input(answer)
        my_ous.append(OU(answer, domain, contents = []))
    for ou in my_ous:
        group_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes the OU {ou} in Domain '{domain}' contain any Groups?\n\n"
                               "Hint:\n"
                               "Groups are collections of Active Directory objects, such as\n"
                               "Users and Computers", f"Create Groups for {ou} in {domain}"))
        if group_response:
            group_list = None
            group_list = create_user_group(ou)
            for group in group_list:
                ou.add_contents(group)
        user_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes the OU {ou} in Domain '{domain}' contain any users?\n\n"
                              "Hint\n"
                              "Users are actual people in the network.", f"Create Users for {ou} in {domain}"))
        if user_response:
            user_list = None
            user_list = create_user_user(ou)
            for user in user_list:
                ou.add_contents(user)
        computer_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes the OU {ou} in Domain '{domain}' contain any computers?\n\n"
                                  "Hint\n"
                                    "Computers can be any network device such as desktops or printers\n"
                                    "or servers.", f"Create Computers for {ou} in {domain}"))
        if computer_response:
            computer_list = None
            computer_list = create_user_computer(ou)
            for computer in computer_list:
                ou.add_contents(computer)
    return my_ous
#a group is similar to an Organizational Unit, except GPOs cannot be applied to groups
def create_user_group(n: Union["OU", "Domain"]) -> list:
    x_button_check(msgbox(f"This program can only work with one level of Groups.\n\nNormally, "
               "you could add Groups to another Group."))
    my_groups = None
    my_groups = []
    container_list = format_container_list(n)
    group_count_message = x_button_check(buttonbox(f"Current Location:\n{container_list}\n\nHow many Groups are in {n}?", f"Create Groups for {n}", ("1 Group", "2 Groups")))
    group_count = int((group_count_message.split())[0])
    for group in range(group_count):
        good_answer = False
        while good_answer == False:
            answer = x_button_check(enterbox(f"Current Location:\n{container_list}\n\nWhat is the name of Group number {group + 1} in {n}"))
            good_answer = check_OU_group_user_computer_input(answer)
        my_groups.append(Group(answer, n, contents = []))
    for group in my_groups:
        user_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes the Group {group} in {n} contain any users?\n\n"
                              "Hint:\n"
                              "Users are actual people in the network.", f"Create Users for {group}"))
        if user_response:
            user_list = None
            user_list = create_user_user(group)
            for user in user_list:
                group.add_contents(user)
        computer_response = x_button_check(ynbox(f"Current Location:\n{container_list}\n\nDoes the Group {group} in {n} contain any computers?\n\n"
                                  "Hint:\n"
                                    "Computers can be any network device such as desktops or printers\n"
                                    "or servers.", f"Create Computers for {group}"))
        if computer_response:
            computer_list = None
            computer_list = create_user_computer(group)
            for computer in computer_list:
                group.add_contents(computer)
    return my_groups
        
def create_user_user(n: Union["Domain", "OU", "Group"]) -> list:
    my_users = None
    my_users = []
    container_list = format_container_list(n)
    user_count_message = x_button_check(buttonbox(f"Current Location:\n{container_list}\n\nHow many Users are in {n}?", f"Create Users for {n}", ("1 User", "2 Users")))
    user_count = int((user_count_message.split())[0])
    for user in range(user_count):
        good_answer = False
        while good_answer == False:
            answer = x_button_check(enterbox(f"Current Location:\n{container_list}\n\nWhat is the name of User number {user + 1}"))
            good_answer = check_OU_group_user_computer_input(answer)
        my_users.append(User(answer, n, contents = []))
    return my_users

def create_user_computer(n: Union["Domain", "OU", "Group"]) -> list:
    my_computers = None
    my_computers = []
    container_list = format_container_list(n)
    computer_count_message = x_button_check(buttonbox(f"Current Location:\n{container_list}\n\nHow many Computers are in {n}?", f"Create Computers for {n}", ("1 Computer", "2 Computers")))
    computer_count = int((computer_count_message.split())[0])
    for user in range(computer_count):
        good_answer = False
        while good_answer == False:
            answer = x_button_check(enterbox(f"Current Location:\n{container_list}\n\nWhat is the name of Computer number {user + 1}"))
            good_answer = check_OU_group_user_computer_input(answer)
        my_computers.append(User(answer, n, contents = []))
    return my_computers
#this function checks the user input when creating a Forest
def check_forest_input(input):
    if input == "":
        x_button_check(msgbox("You must enter a name."))
        return False
    tldn = ["com", "org", "net", "int", "edu", "gov", "mil"]
    try:
        website, tldn_string = input.split(".")
    except ValueError:
        x_button_check(msgbox("Your input must be in top level domain format.\n\n"
               "Example:\n"
               "hardware.com"))
        return False 
    if tldn_string in tldn:
        return True
    else:
        x_button_check(msgbox("Your domain must use one of these top-level domains:\n"
               ".com, .org, .net, .int, .edu, .gov, .mil"))
        return False
#Checks the input when creating a Child.  Since a Child's name must be contiguous with the Tree, we must check it.   
def check_child_input(child, tree):
    if child == "":
        x_button_check(msgbox(f"You Must enter a name."))
        return False
    try:
        c_name, t_name, tldn = child.split(".")
    except ValueError:
        x_button_check(msgbox("Your input must be in the format:\n\n"
                              f"xxx.{tree}"))
        return False
    ts_name, ts_tldn = tree.name.split(".")
    if t_name != ts_name:
        x_button_check(msgbox(f"The Tree domain of the child:\n"
                              f"{t_name}"
                              "Does not equal the Tree name:\n"
                              f"{ts_name}"))
        return False
    if tldn != ts_tldn:
        x_button_check(msgbox(f"The Top Level Domain of the child:\n"
                              f"{t_name}"
                              "Does not equal the Top Level Domain of the Tree:\n"
                              f"{ts_name}"))
        return False
    return True
#checks for OU, group, user, computer object name input    
def check_OU_group_user_computer_input(input):
    if input == "":
        x_button_check(msgbox(f"You Must enter a name."))
        return False
    return True
#this should be an unnecessary function.  EasyGUI does not close when the user presses 'X' or 'Cancel'
# This function exits the program if it detects either of these inputs    
def x_button_check(input):
    if input == None:
        sys.exit()
    else:
        return input
    

#this creates a dictionary so that we can print the AD to a JSON file
def create_new_dict(n):
    new_dict = {}
    for item in n:
        #I had trouble with the type() method on my custom classes, so I extracted the type manually.
        match str(type(item)):
            case "<class 'ADCreatorClasses.Forest'>":
                item_type = "Forest"
            case "<class 'ADCreatorClasses.Tree'>":
                item_type = "Tree"
            case "<class 'ADCreatorClasses.Child'>":
                item_type = "Child"
            case "<class 'ADCreatorClasses.Domain'>":
                item_type = "Domain"
            case "<class 'ADCreatorClasses.OU'>":
                item_type = "OU"
            case "<class 'ADCreatorClasses.Group'>":
                item_type = "Group"
            case "<class 'ADCreatorClasses.User'>":
                item_type = "User"
            case "<class 'ADCreatorClasses.Computer'>":
                item_type = "Computer"
        if item.contents != []:
            #due to the nature of my custom classes, Recursion is possible
            #each object has information for moving up and down so that a recursive function like this can work
            new_dict.update({f"{item_type}-> {item}": create_new_dict(item.contents)})
        else:
            new_dict.update({f"{item_type}-> {item}": ""})
    return new_dict
#creates a list of an objects containers, from immediate to top level
def get_container_list(n: Union["Forest", "Tree", "Child", "Domain", "OU", "Group", "User", "Computer"]) -> list:
    container_list = []
    new_list = []
    if n.container != None:
        container_list.append(n)
        #recursion once again
        container_list.append(get_container_list(n.container))
        #since each recursive call returns a list, I had to modify the list with .extend to prevent nesting
        new_list.append(container_list[0])
        new_list.extend(container_list[1])
    else:
        container_list.append(n)
        new_list.append(container_list[0])
    return new_list
#for some reason, iterating over a list of custom class objects and using xxx.name would not work
#i created this function to extract the str names of each object
def translate_container_list(n: list) -> list:
    new_list = []
    my_range = range(len(n))
    for i in my_range:
        new_list.append(n[i].name)
    return new_list
#this function calls get_container_list and translate_container_list and uses both to produce a custom list
#of an objects type and name.  The order in the list refers to how far up the hierarchy the container is for the given
#input n
#this custom list allows the user to see where the he is currently working in the Active directory
def format_container_list(n: Union["Forest", "Tree", "Child", "Domain", "OU", "Group", "User", "Computer"]) -> list:
    object_list = get_container_list(n)
    name_type_list = []
    type_list = []
    for item in object_list:
        match str(type(item)):
            case "<class 'ADCreatorClasses.Forest'>":
                type_list.append("Forest")
            case "<class 'ADCreatorClasses.Tree'>":
                type_list.append("Tree")
            case "<class 'ADCreatorClasses.Child'>":
                type_list.append("Child")
            case "<class 'ADCreatorClasses.Domain'>":
                type_list.append("Domain")
            case "<class 'ADCreatorClasses.OU'>":
                type_list.append("OU")
            case "<class 'ADCreatorClasses.Group'>":
                type_list.append("Group")
            case "<class 'ADCreatorClasses.User'>":
                type_list.append("User")
            case "<class 'ADCreatorClasses.Computer'>":
                type_list.append("Computer")
    name_list = translate_container_list(object_list)
    my_range = range(len(object_list))
    for i in my_range:
        name_type_list.append(f"{type_list[i]} {name_list[i]}")
    return name_type_list
#just says goodbye
def goodbye():
    x_button_check(msgbox("Your Active Directory has been saved as a JSON.\n\n"
                          "Goodbye."))





        





    
