import json
from faker import Faker
import re
with open('arrets.json', 'r') as arrets:
    data = json.load(arrets)

print(len(data))

charByLastName = dict()


def find_anonymised_names(arret):
    # Use regular expression to find uppercase letters surrounded by square brackets
    # combined_names = re.findall(r'\[([A-Z ]+)\]', arret)
    # combined_names = re.findall(r'\[([A-Z]+(?: [A-Z])+)\]', arret)
    combined_names = re.findall(r'\[([A-Z])\](?: \[([A-Z])\])+', arret)
    # combined_names = re.findall(r'\[([A-Z ]+)\]', arret)
    # combined_names = re.findall(r'\[([A-Z]+(?: [A-Z])+)\]', arret)
    isolated_names = set(re.findall(r'\[([A-Z])\]', arret))
    # titles_and_genres = re.findall(
    #     r'(Monsieur|M\.|Madame|Mme) ([A-Z]+)', arret)
    # print(names_in_brackets, combined_names)
    for combination in combined_names:
        if combination[1] not in charByLastName:
            charByLastName[combination[1]] = dict()
            charByLastName[combination[1]]["first_name"] = [combination[0]]
        else:
            charByLastName[combination[1]]["first_name"].append(combination[0])
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


def replace_letters_with_fake_names(arret, people_by_last_name):
    # print('-------------------------')
    # print(people_by_last_name, arret)
    modif_arret = arret
    for last_name, info in people_by_last_name.items():
        # print(last_name)
        fake = Faker('fr_FR')
        fake_name = fake.last_name()
        # print('-------------------------')
        # print(fake_name, info)
        modif_arret = modif_arret.replace(f"[{last_name}]", fake_name)
        # print(modif_arret)
        if "first_name" in info:

            print('gonna replace first', info.get("first_name"))
            for first_name in info.get('first_name'):
                fake_name = fake.first_name()
                modif_arret = modif_arret.replace(
                    f"[{first_name}]", fake_name)

    # print(modif_arret)
    return modif_arret


def process_arret(arret):
    people_by_last_name = find_anonymised_names(arret)
    modified_arret = replace_letters_with_fake_names(
        arret, people_by_last_name)

    print(modified_arret)
    pass


for arret in data[0]:
    print('new arret')
    charByLastName = dict()
    process_arret(arret.get('text'))
    # print(arret.get('text'))
# print(len(data[0]))
