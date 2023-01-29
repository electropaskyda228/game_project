import random


def generate_level():
    non_rooms = {(50, 50): 'bottom'}
    wh_door = {'top': (-1500, 0), 'bottom': (1500, 0), 'left': (0, 1500), 'right': (0, -1500)}
    rev_doors = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
    ok_rooms = []
    doors = []
    procent = 100
    rooms = []
    doors_1 = []

    while non_rooms:
        n = list(non_rooms.keys())[0]
        for i in wh_door:
            if i == rev_doors[non_rooms[n]]:
                continue
            p = random.randrange(1, 100)
            if p < procent:
                non_rooms[(n[0] + wh_door[i][0], n[1] + wh_door[i][1])] = i
                procent -= 17
                if i == 'top':
                    doors.append((n[0] + 450, n[1] + 300))
                elif i == 'bottom':
                    doors.append((n[0] + 450, n[1]))
                elif i == 'left':
                    doors.append((n[0], n[1] + 300))
                else:
                    doors.append((n[0] + 890, n[1] + 300))

        ok_rooms.append(n)
        non_rooms.pop(n)
    for i in ok_rooms:
        rooms.append(Tile('room', i[0], i[1]))
    for i in doors:
        doors_1.append(Tile('door', i[0], i[1]))
    return rooms, doors_1
