import json
with open('arrets.json', 'r') as arrets:
    data = json.load(arrets)

print(len(data))

for arret in data[0]:
    print(arret.get('text'))
print(len(data[0]))
