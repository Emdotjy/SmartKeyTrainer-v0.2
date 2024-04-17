import pychord
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

def midi_position_to_note_name(midi_position):
    mod_value = (midi_position-21)%12
    value_to_letter = {0: 'A', 1: 'Bb', 2: 'B', 3: 'C', 4: 'Db', 5: 'D', 6: 'Eb', 7: 'E', 8: 'F', 9: 'Gb', 10: 'G', 11: 'Ab'}
    return f"{value_to_letter[mod_value]}"

def chord_name_from_set(entry_set):
    chord = list(entry_set)
    chord.sort()
    res = []
    for note in chord:
        res.append(midi_position_to_note_name(note))
    return(pychord.find_chords_from_notes(res))
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
    print(chord_name_from_set({60,64,67}))
    print(chord_name_from_set({60,64,67,71}))
    print(chord_name_from_set({60,64,67,71,74}))
    print(chord_name_from_set({60,64,68}))
    print(chord_name_from_set({60,64,68,71}))

          