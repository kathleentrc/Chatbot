import re
from pyswip import Prolog

prolog = Prolog()
prolog.consult("family.pl")

relationships = ["sister", 
                 "brother", 
                 "siblings",
                 "mother",
                 "father",
                 "daughter",
                 "son",
                 "parent",
                 "child",
                 "aunt",
                 "uncle",
                 "cousin",
                 "grandfather",
                 "grandmother",
                 "grandchild",
                 "aunt_or_uncle"]

# function to check if a relationship exists between two names
def is_existing_relation(relation, name1, name2):
    query = f"{relation}({name1.lower()}, {name2.lower()})"
    return bool(list(prolog.query(query)))

def unique_relationship(relationship, name):
    query = f"findall(X, {relationship}(X, {name.lower()}), Relationship), length(Relationship, Length)"
    length = list(prolog.query(query))
    #print(relationship + " " + str(length[0]["Length"]))
    #print(length)
    return length[0]["Length"]

def are_related(excluded, inverse_excluded, name1, name2):
    relations_copy = relationships.copy()
    relations_inverse = relationships.copy()

    for e in excluded:
        relations_copy.remove(e)

    for ie in inverse_excluded:
        relations_inverse.remove(ie)
    
    for relationship in relations_copy:
        if is_existing_relation(relationship, name1, name2):
            #print(f"{relationship}: {name1} and {name2}")
            #print("Regular Relationship")
            return False

    for relationship in relations_inverse:
        if is_existing_relation(relationship, name2, name1):
            #print(f"{relationship}: {name2} and {name1}")
            #print("Inverse Relationship")
            return False

    return True

# function to check if a given name has a specified gender and relationship
def is_valid_gender(name, gender):
    query = f"{gender.lower()}({name.lower()})"
    try:
        result = list(prolog.query(query))
        return bool(result)
    except Exception as e:
        print(f"Error: {e}")
        return False
    
# function to checking
def person_exists(name, rs):
    query = f"{rs.lower()}({name.lower()})"
    try:
        result = list(prolog.query(query))
        return bool(result)
    except Exception as e:
        print(f"Error: {e}")
        return False

# function to print children of a parent
def print_children_of_parent(parent_name):
    query = f"child(Child, {parent_name.lower()})"
    children = list(prolog.query(query))
    if children:
        child_names = set([child['Child'].capitalize() for child in children])
        print(f"The children of {parent_name} are: {', '.join(child_names)}.")
    else:
        print(f"{parent_name} has no children.")

def print_daughters_of_parent(parent_name):
    query = f"daughter(Daughter, {parent_name.lower()})"
    daughters = list(prolog.query(query))
    if daughters:
        daughter_names = set([daughter['Daughter'].capitalize() for daughter in daughters])
        print(f"The daughters of {parent_name} are: {', '.join(daughter_names)}.")
    else:
        print(f"{parent_name} has no known daughters.")

def print_sons_of_parent(parent_name):
    query = f"son(Son, {parent_name.lower()})"
    sons = list(prolog.query(query))
    if sons:
        sons_names = set([son['Son'].capitalize() for son in sons])
        print(f"The sons of {parent_name} are: {', '.join(sons_names)}.")
    else:
        print(f"{parent_name} has no known sons.")

def print_siblings(sibling_name):
    query = f"siblings(Sibling, {sibling_name.lower()})"
    siblings = list(prolog.query(query))
    if siblings:
        sibling_names = set([sibling['Sibling'].capitalize() for sibling in siblings])
        print(f"The siblings of {sibling_name} are: {', '.join(sibling_names)}.")
    else:
        print(f"{sibling_name} has no known siblings.")

def print_sisters(sibling_name):
    query = f"sister(Sister, {sibling_name.lower()})"
    sisters = list(prolog.query(query))
    if sisters:
        sister_names = set([sisters['Sister'].capitalize() for sisters in sisters])
        print(f"The sisters of {sibling_name} are: {', '.join(sister_names)}.")
    else:
        print(f"{sibling_name} has no known sisters.")

def print_brothers(sibling_name):
    query = f"brother(Brother, {sibling_name.lower()})"
    brothers = list(prolog.query(query))
    if brothers:
        brother_names = set([brother['Brother'].capitalize() for brother in brothers])
        print(f"The brothers of {sibling_name} are: {', '.join(brother_names)}.")
    else:
        print(f"{sibling_name} has no known brothers.")

def print_mother(child_name):
    query = f"mother(Mother, {child_name.lower()})"
    mothers = list(prolog.query(query))
    if mothers:
        mother_names = set([mother['Mother'].capitalize() for mother in mothers])
        if len(mother_names) == 1:
            print(f"The mother of {child_name} is {', '.join(mother_names)}.")
        else:
            print(f"The mothers of {child_name} are: {', '.join(mother_names)}.")
    else:
        print(f"{child_name} has no known mother/s.")

def print_father(child_name):
    query = f"father(Father, {child_name.lower()})"
    fathers = list(prolog.query(query))
    if fathers:
        father_names = set([father['Father'].capitalize() for father in fathers])
        if len(father_names) == 1:
            print(f"The father of {child_name} is {', '.join(father_names)}.")
        else:
            print(f"The fathers of {child_name} are: {', '.join(father_names)}.")
    else:
        print(f"{child_name} has no known father/s.")

def print_parents(child_name):
    query = f"parent(Parent, {child_name.lower()})"
    parents = list(prolog.query(query))
    parent_names = []
    query = f"father(Father, {child_name.lower()})"
    fathers = list(prolog.query(query))
    father_names = []
    query = f"mother(Mother, {child_name.lower()})"
    mothers = list(prolog.query(query))
    mother_names = []

    if parents:
        parent_names = [parent['Parent'].capitalize() for parent in parents]
    if fathers:
        father_names = [father['Father'].capitalize() for father in fathers]
    if mothers:
        mother_names = [mother['Mother'].capitalize() for mother in mothers]

    parent_names.extend(father_names)
    parent_names.extend(mother_names)
    all_parents = set(parent_names)

    if len(all_parents) == 1:
        print(f"The parent of {child_name} is {', '.join(all_parents)}.")
    elif len(all_parents) > 1:
        print(f"The parents of {child_name} are: {', '.join(all_parents)}.")
    else:
        print(f"{child_name} has no known parent/s.")


def update_gender(individual, new_gender):
    query = f"retract(genderless({individual.lower()})), assertz({new_gender}({individual}))."
    list(prolog.query(query))



# function to process the input sentence and update the Prolog knowledge base
def process_sentence(sentence):
    # extract names from the sentence using a regular expression
    names = re.findall(r'\b[A-Z][a-z]*\b', sentence)

    # check for sibling relationships
    if "siblings" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert sibling relationship if names are different
                excluded = ["siblings", "brother", "sister"]
                inverse_excluded = ["siblings", "brother", "sister"]
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if not is_existing_relation("siblings", names[0], names[1]):
                        prolog.assertz("siblings(" + names[0].lower() + ", " + names[1].lower() + ")")    
                        prolog.assertz("siblings(" + names[1].lower() + ", " + names[0].lower() + ")")

                        if not is_valid_gender(names[0], "male") and not is_valid_gender(names[0], "female"):
                            prolog.assertz("genderless(" + names[0].lower() + ")")
                        if not is_valid_gender(names[1], "male") and not is_valid_gender(names[1], "female"):
                            prolog.assertz("genderless(" + names[1].lower() + ")")

                        print("OK! I learned something.")
                    else:
                        print(f"{names[0]} and {names[1]} are already siblings.")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if "Who" in sentence:
                sibling_name = re.search(r'siblings of (\w+)', sentence, re.IGNORECASE)
                if sibling_name.group(1):
                    print_siblings(sibling_name.group(1))
                else:
                    return False
                return True
            if len(names) == 2:
                # check if sibling relationship exists and print the result
                    if is_existing_relation("siblings", names[0], names[1]):
                        print("Yes!")
                    else:
                        print("No!")
                    return True
            else:
                return False
    
    # check for sister relationships
    elif "sister" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert sister relationship if names are different
                excluded = ["siblings", "sister"]
                inverse_excluded = ["siblings", "brother", "sister"]
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "female") or is_valid_gender(names[0], "genderless") or not person_exists(names[0], "person"):
                        if not is_existing_relation("sister", names[0], names[1]):
                            prolog.assertz("sister(" + names[0].lower() + ", " + names[1].lower() + ")")

                            if is_valid_gender(names[0], "genderless"):
                                update_gender(names[0], "female")
                            else:
                                prolog.assertz("female(" + names[0].lower() + ")")

                            prolog.assertz("person(" + names[0].lower() + ")")
                            print("OK! I learned something.")
                        else:
                            print(f"{names[0]} is already the sister of {names[1]}.")
                    else:
                        print("That's impossible!")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if "Who" in sentence:
                sibling_name = re.search(r'sisters of (\w+)', sentence, re.IGNORECASE)
                if sibling_name.group(1):
                    print_sisters(sibling_name.group(1))
                else:
                    return False
                return True
            if len(names) == 2:
                if is_valid_gender(names[0], "genderless") and is_existing_relation("siblings", names[0], names[1]):
                    print("Not enough information to determine sibling's gender.") 
                elif is_existing_relation("sister", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    # check for brother relationships
    elif "brother" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert brother relationship if names are different
                excluded = ["siblings", "brother"]
                inverse_excluded = ["siblings", "brother", "sister"]
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "male") or not person_exists(names[0], "person"):
                        if not is_existing_relation("brother", names[0], names[1]):
                            prolog.assertz("brother(" + names[0].lower() + ", " + names[1].lower() + ")")

                            if is_valid_gender(names[0], "genderless"):
                                update_gender(names[0], "male")
                            else:
                                prolog.assertz("male(" + names[0].lower() + ")")
                            
                            prolog.assertz("person(" + names[0].lower() + ")")
                            print("OK! I learned something.")
                        else:
                            print(f"{names[0]} is already the brother of {names[1]}.")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if "Who" in sentence:
                sibling_name = re.search(r'brothers of (\w+)', sentence, re.IGNORECASE)
                if sibling_name.group(1):
                    print_brothers(sibling_name.group(1))
                else:
                    return False
                return True
            if len(names) == 2:
                    if is_valid_gender(names[0], "genderless") and is_existing_relation("siblings", names[0], names[1]):
                        print("Not enough information to determine sibling's gender.") 
                    elif is_existing_relation("brother", names[0], names[1]):
                        print("Yes!")
                    else:
                        print("No!")
                    return True
            else:
                return False
        
    # check for grandfather relationships
    elif "grandfather" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["grandfather"]
                inverse_excluded = ["grandchild"]
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "male") or not person_exists(names[0], "person"):
                        if not is_existing_relation("grandfather", names[0], names[1]):
                            if unique_relationship("grandfather", names[1]) < 2:
                                prolog.assertz("grandfather(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz(f"male({names[0].lower()})")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something.")
                            else:
                                print("That's impossible!")
                        else:
                            print(f"{names[0]} is already a grandfather of {names[1]}.")
                            
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if grandfather relationship exists and print the result
                if is_existing_relation("grandfather", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    # check for grandmother relationships
    elif "grandmother" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert grandmother relationship if names are different
                excluded = ["grandmother"]
                inverse_excluded = ["grandchild"]
                inverse_excluded = []
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "female") or not person_exists(names[0], "person"):
                        if not is_existing_relation("grandmother", names[0], names[1]):
                            if unique_relationship("grandmother", names[1]) < 2:
                                prolog.assertz("grandmother(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz("female(" + names[0].lower() + ")")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something.")
                            else:
                                print("That's impossible!")
                        else:
                            print(f"{names[0]} is already a grandmother of {names[1]}.")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if grandmother relationship exists and print the result
                if is_existing_relation("grandmother", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False
        
    # check for parents relationship
    elif "parents" in sentence:
        if "." in sentence:
            if len(names) == 3:
                # assert parents relationship if names are different
                excluded = ["parent", "mother", "father"]
                inverse_excluded = ["child", "son", "daughter"]
                if len(names) == len(set(names) or not are_related(excluded, names[0], names[1])):
                    if not is_existing_relation("parent", names[0], names[2]) or not is_existing_relation("parent", names[1], names[2]):
                        if unique_relationship("parent", names[2]) == 0 and unique_relationship("father", names[2]) == 0 and unique_relationship("mother", names[2]) == 0:
                            prolog.assertz("parent(" + names[0].lower() + ", " + names[2].lower() + ")")
                            prolog.assertz("parent(" + names[1].lower() + ", " + names[2].lower() + ")")
                            prolog.assertz("person(" + names[0].lower() + ")")
                            prolog.assertz("person(" + names[1].lower() + ")")
                            print("OK! I learned something.")
                            
                            if not is_valid_gender(names[0], "male") and not is_valid_gender(names[0], "female"):
                                prolog.assertz("genderless(" + names[0].lower() + ")")
                            if not is_valid_gender(names[1], "male") and not is_valid_gender(names[1], "female"):
                                prolog.assertz("genderless(" + names[1].lower() + ")")
                        else:
                            print("That's impossible!")

                    else:
                        print(names[0] + " and " + names[1] + " are already parents of " + names[2] + ".")
                else:
                    print("That's impossible!")
                return True
            else:
                return False
        
        elif "?" in sentence:
            names.pop(0)
            if "Who" in sentence:
                child_name = re.search(r'parents of (\w+)', sentence, re.IGNORECASE)
                if child_name.group(1):
                    print_parents(child_name.group(1))
                else:
                    return False
                return True
            if len(names) == 3:
                    if is_existing_relation("parent", names[0], names[2]) and is_existing_relation("parent", names[1], names[2]):
                        print("Yes!")
                    else:
                        print("No!")
                    return True
            else:
                return False
        
    # check for mother relationships
    elif "mother" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert mother-child relationship if names are different
                excluded = ["parent", "mother"]
                inverse_excluded = ["child", "daughter", "son"]
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "female") or is_valid_gender(names[0], "genderless") or not person_exists(names[0], "person"):
                        if not is_existing_relation("mother", names[0], names[1]):
                            if unique_relationship("mother", names[1]) == 0 and unique_relationship("parent", names[1]) < 2:
                                if is_valid_gender(names[0], "genderless"):
                                    update_gender(names[0], "female")

                                prolog.assertz("mother(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz(f"female({names[0].lower()})")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something.")
                            else:
                                print("That's impossible!")
                        else:
                            print("She is already their mother.")
                    else:
                        print("That's impossible!")
                else:
                    print("That's impossible!")
                return True
            else:
                return False
            
        elif "?" in sentence:
            names.pop(0)
                # check if mother relationship exists and print the result
            if "Who" in sentence:
                child_name = re.search(r'mother of (\w+)', sentence, re.IGNORECASE)
                if child_name.group(1):
                    print_mother(child_name.group(1))
                else:
                    return False
                return True
            if len(names) == 2:
                if is_valid_gender(names[0], "genderless") and is_existing_relation("parent", names[0], names[1]):
                    print("Not enough information to determine parent's gender.") 
                elif is_existing_relation("mother", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    # check for father relationships
    elif "father" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert father-child relationship if names are different
                excluded = ["parent", "father"]
                inverse_excluded = ["child", "daughter", "son"]
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "male") or is_valid_gender(names[0], "genderless") or not person_exists(names[0], "person"):
                        if not is_existing_relation("father", names[0], names[1]):
                            if unique_relationship("father", names[1]) == 0 and unique_relationship("parent", names[1]) < 2:
                                if is_valid_gender(names[0], "genderless"):
                                    update_gender(names[0], "male")

                                prolog.assertz("father(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz(f"male({names[0].lower()})")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                #print(bool(list(prolog.query(f"male({names[0].lower()})"))))
                                print("OK! I learned something.")
                            else:
                                print("That's impossible!")
                        else:
                            print("He is already their father.")
                    else:
                        print("That's impossible!")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            # check if father relationship exists and print the result
            if "Who" in sentence:
                child_name = re.search(r'father of (\w+)', sentence, re.IGNORECASE)
                if child_name.group(1):
                    print_father(child_name.group(1))
                else:
                    return False
                return True
            if len(names) == 2:
                    if is_valid_gender(names[0], "genderless") and is_existing_relation("parent", names[0], names[1]):
                        print("Not enough information to determine parent's gender.") 
                    elif is_existing_relation("father", names[0], names[1]):
                        print("Yes!")
                    else:
                        print("No!")
                    return True
            else:
                return False

    # check for daughter relationships
    if "daughter" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["child", "daughter"]
                inverse_excluded = ["parent", "mother", "father"]
                # assert daughter relationship if names are different and have valid genders
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "female") or is_valid_gender(names[0], "genderless") or not person_exists(names[0], "person"):
                        if not is_existing_relation("daughter", names[0], names[1]):
                            if (unique_relationship("mother", names[0]) == 0 and unique_relationship("father", names[0]) == 0 and unique_relationship("parent", names[0]) < 2) or is_existing_relation("child", names[0], names[1]):
                                prolog.assertz("daughter(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz("female(" + names[0].lower() + ")")
                                prolog.assertz("parent(" + names[1].lower() + ", " + names[0].lower() + ")")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something.")
                            
                            else:
                                print("That's impossible!")
                        else:
                            print(f"{names[0]} is already a daughter of {names[1]}.")
                    else:
                        print("That's impossible!")
                else:
                    print("That's impossible!")
                return True
            else:
                return False
        
        elif "daughters of" in sentence and "?" in sentence:
            parent_name = re.search(r'daughters of (\w+)', sentence, re.IGNORECASE)
            if parent_name.group(1):
                print_daughters_of_parent(parent_name.group(1))
            else:
                return False
            return True

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if daughter relationship exists and print the result
                if is_valid_gender(names[0], "genderless") and is_existing_relation("parent", names[1], names[0]):
                    print("Not enough information to determine child's gender.") 
                elif is_existing_relation("daughter", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    # check for son relationships
    if "son" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["child", "son"]
                inverse_excluded = ["parent", "mother", "father"]
                # assert son relationship if names are different and have valid genders
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "male") or is_valid_gender(names[0], "genderless") or not person_exists(names[0], "person"):
                        if not is_existing_relation("son", names[0], names[1]):
                            if (unique_relationship("mother", names[0]) == 0 and unique_relationship("father", names[0]) == 0 and unique_relationship("parent", names[0]) < 2) or is_existing_relation("child", names[0], names[1]):
                                prolog.assertz("son(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz("male(" + names[0].lower() + ")")
                                prolog.assertz("parent(" + names[1].lower() + ", " + names[0].lower() + ")")

                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something. 1")
                            else:
                                print("That's impossible!")
                        else:
                            print(f"{names[0]} is already a son of {names[1]}.")
                    else:
                        print("That's impossible!")
                else:
                    print("That's impossible!")
                return True
            else:
                return False
        
        elif "sons of" in sentence and "?" in sentence:
            parent_name = re.search(r'sons of (\w+)', sentence, re.IGNORECASE)
            if parent_name.group(1):
                print_sons_of_parent(parent_name.group(1))
            else:
                return False
            return True

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                if is_valid_gender(names[0], "genderless") and is_existing_relation("parent", names[1], names[0]):
                    print("Not enough information to determine child's gender.") 
                elif is_existing_relation("son", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    elif "children" in sentence:
        if "." in sentence:
            excluded = ["child", "daughter", "son"]
            inverse_excluded = ["parent", "mother", "father"]
            learned = False
            related = False
            unique = True
            if len(names) == len(set(names)):
                for n in range(0, len(names) - 1):
                    if not are_related(excluded, inverse_excluded, names[n], names[-1]):
                        related = True
                        break
                    if not is_existing_relation("parent", names[-1], names[n]):
                        if unique_relationship("mother", names[n]) < 2 and unique_relationship("father", names[n]) < 2 and unique_relationship("parent", names[n]) < 2:
                            #prolog.assertz(f"parent({names[-1].lower()}, {names[n].lower()})")
                            prolog.assertz(f"parent({names[-1].lower()}, {names[n].lower()})")
                            prolog.assertz("person(" + names[n].lower() + ")")
                            if not is_valid_gender(names[n], "male") and not is_valid_gender(names[n], "female"):
                                prolog.assertz(f"genderless({names[n].lower()})")

                            if not person_exists(names[-1], "person"):
                                prolog.assertz("person(" + names[-1].lower() + ")")
                                if not is_valid_gender(names[-1], "male") and not is_valid_gender(names[-1], "female"):
                                    prolog.assertz(f"genderless({names[-1].lower()})")
                            learned = True
                        else:
                            unique = False
                            break
                
                if learned:
                    print(f"OK! I learned something.")
                elif related or not unique:
                    print("That's impossible!")
                elif not learned:
                    print("They are already children of " + names[-1] + ".")

            return True

        elif "children of" in sentence and "?" in sentence:
            all_children = True
            if "Are" in sentence:
                names.pop(0)
                for n in range(0, len(names) - 1):
                    if not is_existing_relation("parent", names[-1], names[n]) and not is_existing_relation("child", names[n], names[-1]):
                        all_children = False

                if all_children:
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                parent_name = re.search(r'children of (\w+)', sentence, re.IGNORECASE)
                if parent_name.group(1):
                    print_children_of_parent(parent_name.group(1))
                else:
                    return False
                return True

    # check for child relationships
    elif "child" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["child", "daughter", "son"]
                inverse_excluded = ["parent", "mother", "father"]
                # assert child relationship if names are different
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if not is_existing_relation("parent", names[1].lower(), names[0].lower()):
                        if (unique_relationship("mother", names[0]) == 0 and unique_relationship("father", names[0]) == 0 and unique_relationship("parent", names[0]) < 2) or is_existing_relation("child", names[0], names[1]):
                            #prolog.assertz("parent(" + names[1].lower() + ", " + names[0].lower() + ")")
                            prolog.assertz("parent(" + names[1].lower() + ", " + names[0].lower() + ")")
                            prolog.assertz("person(" + names[0].lower() + ")")

                            if not is_valid_gender(names[0], "male") and not is_valid_gender(names[0], "female"):
                                    prolog.assertz(f"genderless({names[0].lower()})")

                            if not person_exists(names[1], "person"):
                                prolog.assertz("person(" + names[1].lower() + ")")
                                if not is_valid_gender(names[1], "male") and not is_valid_gender(names[1], "female"):
                                    prolog.assertz(f"genderless({names[1].lower()})")

                            print("OK! I learned something.")
                        else:
                            print("That's impossible!")
                    else:
                        print(f"{names[0]} is already a child of {names[1].lower()}")
                else:
                    print("That's impossible!")
                return True
            else:
                return False
            
        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if child relationship exists and print the result
                if is_existing_relation("parent", names[1], names[0]) or is_existing_relation("child", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            return False
        
    # check for aunt relationships
    elif "aunt" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["aunt"]
                inverse_excluded = []
                # assert aunt relationship if names are different
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "female") or is_valid_gender(names[0], "genderless") or not person_exists(names[0], "person"):
                        if unique_relationship("aunt", names[1]) < 2:
                            if not is_existing_relation("aunt", names[0], names[1]):
                                prolog.assertz("aunt(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something.")
                            else:
                                print("She is already their aunt.")
                        else:
                            print("That's impossible!")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if aunt relationship exists and print the result
                if is_existing_relation("aunt", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False
        
    # check for uncle relationships
    elif "uncle" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["uncle"]
                inverse_excluded = []
                # assert aunt relationship if names are different
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if is_valid_gender(names[0], "male") or not person_exists(names[0], "person"):
                        if not is_existing_relation("uncle", names[0], names[1]):
                            if unique_relationship("uncle", names[1]) < 2:
                                prolog.assertz("uncle(" + names[0].lower() + ", " + names[1].lower() + ")")
                                prolog.assertz("male(" + names[0].lower() + ")")
                                prolog.assertz("person(" + names[0].lower() + ")")
                                print("OK! I learned something.")
                            else:
                                print("That's impossible!")
                        else:
                            print("He is already their uncle.")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if aunt relationship exists and print the result
                if is_existing_relation("uncle", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    # check for cousin relationships
    elif "cousin" in sentence:
        if "." in sentence:
            if len(names) == 2:
                excluded = ["cousin"]
                inverse_excluded = []
                # assert cousin relationship if names are different
                if not (names[0].lower() == names[1].lower() or not are_related(excluded, inverse_excluded, names[0], names[1])):
                    if not is_existing_relation("cousin", names[0], names[1]):
                        prolog.assertz("cousin(" + names[0].lower() + ", " + names[1].lower() + ")")
                        print("OK! I learned something.")
                    else:
                        print("They are already cousins.")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if cousin relationship exists and print the result
                if is_existing_relation("cousin", names[0], names[1]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False
        
    # check for relatives relationships
    elif "relatives" in sentence:
        if "." in sentence:
            if len(names) == 2:
                # assert relatives relationship if names are different
                if not (names[0].lower() == names[1].lower()):
                    if not is_existing_relation("relatives", names[0], names[1]):
                        prolog.assertz("relatives(" + names[0].lower() + ", " + names[1].lower() + ")")
                        print("OK! I learned something.")
                    else:
                        print("They are already relatives.")
                else:
                    print("That's impossible!")
                return True
            else:
                return False

        elif "?" in sentence:
            names.pop(0)
            if len(names) == 2:
                # check if relatives relationship exists and print the result
                if is_existing_relation("relatives", names[0], names[1]) or is_existing_relation("relatives", names[1], names[0]):
                    print("Yes!")
                else:
                    print("No!")
                return True
            else:
                return False

    

if __name__ == "__main__":
    print("Enter a prompt below.")
    sentence = " "
    while sentence.lower() != "quit":
        sentence = input("\n> ")
        # Process the input sentence, handle invalid input
        if not process_sentence(sentence) and sentence.lower() != "quit":
            print("Invalid input given.")
