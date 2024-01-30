import json 
with open('dataset.json', 'r') as arrets:
    data = json.load(arrets)

print(len(data))
number_unrecognized_protagonists = 0

for arret in data:
    if not arret.get("protagonistsPositions"):
        number_unrecognized_protagonists+=1
        # print(arret.get("text"))

print(number_unrecognized_protagonists, 'percentage', f"{number_unrecognized_protagonists}/{len(data)}")


def check_no_overlap(arret, intervals):
    # Sort intervals based on the start position
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    # Check for overlap
    for i in range(1, len(sorted_intervals)):
        if sorted_intervals[i][0] < sorted_intervals[i-1][1]:
            print(arret.get("text")[sorted_intervals[i][0]-10:sorted_intervals[i][0]+10],
                sorted_intervals[i-1:i+1], 
                 arret.get("text")[sorted_intervals[i][0]],
                 arret.get("text")[sorted_intervals[i][1]],
                 arret.get("text")[sorted_intervals[i-1][0]],
                 arret.get("text")[sorted_intervals[i-1][1]]
                 )
            return False  # Overlap found

    return True  # No overlap

pb_counter = 0

for arret in data:
    print("--------------------------------------------------------------")
    if not check_no_overlap(arret, arret.get("protagonistsPositions")):
        pb_counter +=1

print(pb_counter)

