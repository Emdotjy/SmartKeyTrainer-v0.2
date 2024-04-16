import random
from utils import     get_midi_value_from_scale, get_scale_value




class Sequence:
    def __init__(
            self,
            suffix='',
            chord_shapes = [{60,64,67}],
            name = "",
            mod = False,
            keep_scale = False,
            scale_type ="Chromatic",
            starting_scale =0,
            shift = 0,
            repetition=0,
            inversion = 0,
            interval = None)->None:
        
        self.mod = mod
        self.current_scale = starting_scale
        self.keep_scale = keep_scale
        self.scale_type =scale_type
        if interval== None:
            self.interval = [0]

        else:
            self.interval = interval
        #the shape of the chords is a set of midi note value (int)
        self.chord_shapes_list = chord_shapes

        self.chord_shapes_progression =0
        self.shift = shift
        self.repetition= repetition
        self.inversion= inversion
        if scale_type == "Major":
            self.scale_dict = {1:0,2:2,3:4,4:5,5:7,6:9,7:11}
        else:
            self.scale_dict = {i:i for i in range(12)}
        
    def get_chord_name(self):
        return str(self.chord_shapes_list[self.chord_shapes_progression])

    def get_targets(self):
        if self.mod:
            mod_notes = set()
            for number_set in self.chord_shapes_list:
                mod_notes.update({num %12 for num in number_set} )
            i=0
            target_notes = set()
            while target_notes == set() or max(target_notes) <108:
                target_notes.update({n+12*i for n in mod_notes})
                i=i+1
            print(self.interval)
            target_notes.intersection_update(self.interval[0],self.interval[0])
        else:
            target_notes = self.chord_shapes_list[self.chord_shapes_progression]
        return target_notes
                            
    def target_reached(self,notes)-> bool:

        if notes == self.chord_shapes_list[self.chord_shapes_progression] or (notes%12 == self.chord_shapes_list[self.chord_shapes_progression] and self.mod):
            
            self.chord_shapes_progression+=1
            print(self.chord_shapes_progression)
            print(len(self.chord_shapes_list))
            if self.chord_shapes_progression == len(self.chord_shapes_list):
                self.chord_shapes_progression=0
                if not self.keep_scale:
                    self.shift_shape()
                else:
                    self.shift_shape_in_scale()
            return True
        return False

            
    def shift_shape(self):
        if self.shift==0:
            shift = random(1,11)
        else:
            shift = self.shift
        self.chord_shapes_list = [{num + shift for num in number_set} for number_set in self.chord_shapes_list]
    
    def shift_shape_in_scale(self):
        if self.shift==0:
            shift = random(1,11)
        else:
            shift = self.shift
            print("shift in scale")
        chords_scale_values = get_scale_value(self.current_scale ,self.chord_shapes_list)
        print(chords_scale_values)
        chords_scale_values_shifted = [{num + shift for num in number_set} for number_set in chords_scale_values]
        print(chords_scale_values_shifted)
        self.chord_shapes_list= get_midi_value_from_scale(self.current_scale ,chords_scale_values_shifted)
        print(self.chord_shapes_list)