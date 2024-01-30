import json
from arret import Arret
from faker import Faker
import re
with open('arrets.json', 'r') as arrets:
    data = json.load(arrets)

print(len(data))

charByLastName = dict()
dataset = []


def find_anonymised_names(arret: Arret):
    # Use regular expression to find uppercase letters surrounded by square brackets
    # combined_names = re.findall(r'\[([A-Z ]+)\]', arret)
    # combined_names = re.findall(r'\[([A-Z]+(?: [A-Z])+)\]', arret)
    arret_text = arret.text
    combined_names = re.findall(r'\[([A-Z])\](?: \[([A-Z])\])+', arret_text)
    # combined_names = re.findall(r'\[([A-Z ]+)\]', arret)
    # combined_names = re.findall(r'\[([A-Z]+(?: [A-Z])+)\]', arret)
    isolated_names = set(re.findall(r'\[([A-Z])\]', arret_text))
    # titles_and_genres = re.findall(
    #     r'(Monsieur|M\.|Madame|Mme) ([A-Z]+)', arret)
    # print(names_in_brackets, combined_names)
    for combination in combined_names:
        if combination[1] not in charByLastName:
            charByLastName[combination[1]] = dict()
            charByLastName[combination[1]]["first_name"] = dict()
            charByLastName[combination[1]]["first_name"][combination[0]] = None
        else:
            charByLastName[combination[1]]["first_name"][combination[0]] = None
        if combination[0] in isolated_names:
            isolated_names.remove(combination[0])

    for name in isolated_names:
        if not name in charByLastName:
            charByLastName[name] = dict()
            # charByLastName[name] = None
        # charByLastName[combined_names[1]] = combined_names[0]

    # print(charByLastName)
    # Convert the list of letters to a string
    # names = ''.join(names_in_brackets)

    # print(names, arret[:1000])
    # if isolated_names:
    #     print(arret)
    return charByLastName


red = "\033[31m"
green = "\033[32m"
blue = "\033[34m"
reset = "\033[39m"


def replace_letters_with_fake_names(arret: Arret, people_by_last_name):
    # print('-------------------------')
    # print(people_by_last_name, arret)
    for last_name, info in people_by_last_name.items():
        # print(last_name)
        fake = Faker('fr_FR')
        fake_name = fake.last_name()
        fake_name_with_color = red + " " + fake_name + " "+reset
        arret.text = arret.text.replace(
            f"[{last_name}]", fake_name)
        people_by_last_name[last_name]["fake_last_name"] = fake_name
        if "first_name" in info:

            print('gonna replace first', info.get("first_name"))
            for first_name in info.get('first_name').keys():
                fake_name = fake.first_name()
                fake_name_with_color = green + " " + fake_name + " "+reset
                arret.text = arret.text.replace(
                    f"[{first_name}]", fake_name)
                people_by_last_name[last_name]["first_name"][first_name] = fake_name

    # print(modif_arret,sep="NNNNNNNNNNNNNNNNNNNNNN")
    # arret.text = modif_arret
    find_protagonists_positions(people_by_last_name, arret)
    return arret


import sys

def find_protagonists_positions(people_by_last_name, arret: Arret):
    # print(people_by_last_name, arret.text)
    for last_name, info in people_by_last_name.items():
        # print(last_name,info, 'ce qu on cherche',people_by_last_name[last_name]["fake_last_name"])
        # try:
        for match in re.finditer(fr'\b{re.escape(people_by_last_name[last_name]["fake_last_name"])}\b', arret.text):
            arret.protagonistsPositions.append((match.start(), match.end()))
        if "first_name" in info:
            # try:
            for first_name, fake_first_name in info.get('first_name').items():
                for match in re.finditer(rf'\b{re.escape(fake_first_name)}\b', arret.text):
                    arret.protagonistsPositions.append(
                        (match.start(), match.end()))
            # except:
            #     print(arret.text, last_name, info,sep="-----------------")
            #     sys.exit()


def process_arret(arret: Arret):
    people_by_last_name = find_anonymised_names(arret)
    modified_arret = replace_letters_with_fake_names(
        arret, people_by_last_name)

    return modified_arret

dataset = []

print(len(data[:10][0][:10]))
for arretDict in data[:10][0]:
    print('new arret')
    arret = Arret(identifier=arretDict.get('id'), text=arretDict.get('text'))
    charByLastName = dict()
    modif_arret = process_arret(arret)
    dataset.append(modif_arret)


# Serializing json
json_object = json.dumps(dataset, indent=4, default=lambda obj: obj.__dict__)

with open("dataset2.json", "w") as outfile:
    outfile.write(json_object)
    
