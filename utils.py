# Define the frequency of each note
notes_freq = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25
}
major_scale = [0,2,4,5,7,9,11]



#scale is a value between 0 and 11
def get_scale_value(scale,chord_shapes_list):
    res = []
    chord  = set()
    print(scale,chord_shapes_list)
    for chord_shape in chord_shapes_list:
        chord.clear()
        print(res)
        for note in chord_shape:
            note_scale_octave_value = (note-scale)//12
            print("3")
            try:    
                note_scale_degree = major_scale.index((note-scale)%12)
            except:
                print("note not in scale,unable to assign scale value")

            chord.add(note_scale_degree+note_scale_octave_value*7)
        res.append(chord)
    return res
    

def get_midi_value_from_scale(scale,chord_shapes_list):
    res = []
    chord  = set()
    for chord_shape in chord_shapes_list:
        chord.clear()
        for note in chord_shape:
            note_scale_octave_value = (note-scale)//7
            note_chromatic_degree = major_scale[(note-scale)%7]

            chord.add(scale+note_chromatic_degree+note_scale_octave_value*12)
        res.append(chord)
    return res

if __name__ == "__main__":
    print(get_scale_value(0,[{21,22,23,24,25,26,27,28}]))
    print(get_midi_value_from_scale(0,get_scale_value(0,[{21,22,23,24,25,26,27,28}]))        )