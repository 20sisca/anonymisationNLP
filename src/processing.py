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
            charByLastName[combination[1]]["first_name"] = set(combination[0])
        else:
            charByLastName[combination[1]]["first_name"].add(combination[0])
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
    modif_arret = arret.text
    for last_name, info in people_by_last_name.items():
        # print(last_name)
        fake = Faker('fr_FR')
        fake_name = fake.last_name()
        fake_name_with_color = red + " " + fake_name + " "+reset
        # print('-------------------------')
        # print(fake_name, info)
        modif_arret = modif_arret.replace(
            f"[{last_name}]", last_name + " "+fake_name_with_color)
        print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', re.findall(
            fr'\b{re.escape(fake_name)}\b', modif_arret, flags=re.IGNORECASE))
        for match in re.finditer(fr'\b{re.escape(fake_name)}\b', modif_arret):

            arret.protagonistsPositions.append((match.start(), match.end()))
        # print(modif_arret)
        if "first_name" in info:

            print('gonna replace first', info.get("first_name"))
            for first_name in info.get('first_name'):
                fake_name = fake.first_name()
                fake_name_with_color = green + " " + fake_name + " "+reset
                print('NNNNNNNN', fake_name)
                modif_arret = modif_arret.replace(
                    f"[{first_name}]", first_name+" "+fake_name_with_color)

                print('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', re.findall(
                    fr'\b{re.escape(fake_name)}\b', modif_arret, flags=re.IGNORECASE))
                for match in re.finditer(rf'\b{re.escape(fake_name)}\b', modif_arret):

                    arret.protagonistsPositions.append(
                        (match.start(), match.end()))
    # print(modif_arret)
    return modif_arret


def process_arret(arret: Arret):
    people_by_last_name = find_anonymised_names(arret)
    modified_arret = replace_letters_with_fake_names(
        arret, people_by_last_name)

    print(modified_arret)
    pass


for arretDict in data[0]:
    print('new arret')
    arret = Arret(identifier=arretDict.get('id'), text=arretDict.get('text'))
    charByLastName = dict()
    process_arret(arret)
    print(arret.protagonistsPositions)
    # print(arret.get('text'))
# print(len(data[0]))
