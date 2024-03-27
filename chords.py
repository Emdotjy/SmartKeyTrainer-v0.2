import mido
import random


def generate_seventh_chord():
    fundamental = random.choice([["C",0],["D",2],["E",4],["F",5],["G",7],["A",9],["B",11]])
    alt = random.choice(["b","","#"])
    chord_type = random.choice(["m7","maj7","7"])
    
    fundamental[0] = fundamental[0] + alt
    if alt == "b":
        fundamental[1] = (fundamental[1]-1)%12
    elif alt == "#":
        fundamental[1] = (fundamental[1]+1)%12

    if chord_type == "m7":
        increments = [3,4,3]
    elif chord_type == "maj7":
        increments = [4,3,4]
    elif chord_type == "7":
        increments = [4,3,3]

    pointer = fundamental[1]
    chord = set()
    chord.add(pointer	)
    for i in increments:
        pointer = (pointer+i)%12
        chord.add(pointer)
    return [fundamental[0]+chord_type,[chord]]
    


def generate_AB_voicing():
    fundamental = random.choice([["C",0],["D",2],["E",4],["F",5],["G",7],["A",9],["B",11]])
    alt = random.choice(["b","","#"])
    chord_type = random.choice(["m7","maj7","7"])
    
    fundamental[0] = fundamental[0] + alt
    if alt == "b":
        fundamental[1] = (fundamental[1]-1)%12
    elif alt == "#":
        fundamental[1] = (fundamental[1]+1)%12

    
    if chord_type == "m7":
        pointer_A  = (fundamental[1]+3)%12+48
        pointer_B= (fundamental[1]+10)%12+48
        increments_A = [7,4,5]
        increments_B = [5,4,7]
        
    elif chord_type == "maj7":
        pointer_A   = (fundamental[1]+4)%12+48
        pointer_B  = (fundamental[1]+11)%12+48
        increments_A = [7,3,5]
        increments_B = [5,3,7]
    elif chord_type == "7":
        pointer_A   = (fundamental[1]+4)%12+48
        pointer_B  = (fundamental[1]+10)%12+48
        increments_A = [6,4,5]
        increments_B = [6,5,7]
   
    chord_A = set()
    chord_A.add(pointer_A	)
    chord_B = set()
    chord_B.add(pointer_B	)
    for i in increments_A:
        pointer_A = (pointer_A+i)
        chord_A.add(pointer_A)
    for i in increments_B:
        pointer_B = (pointer_B+i)
        chord_B.add(pointer_B)
    return fundamental[0]+chord_type,[chord_A,chord_B]

