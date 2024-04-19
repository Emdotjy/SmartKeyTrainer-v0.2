import time
import rtmidi
import random
import mido
import chords
from SmartKeyTrainerUI import SmartKeyTrainerUI
from audio_handler import *
import threading
import tkinter as tk
from TargetGenerator import TargetGenerator

class SmartKeyTrainer:
    "Main class for the SmartKeyTrainer application."
    
    def select_midi(self, items):
        def on_select(event):
            selected_item = listbox.get(listbox.curselection())
            print("Selected item:", selected_item)
            root.destroy()
            self.input_name = selected_item
        root = tk.Tk()
        root.title("Select midi input")
        listbox = tk.Listbox(root)
        listbox.pack()       
        for item in items:
            listbox.insert(tk.END, item)
        listbox.bind("<<ListboxSelect>>", on_select)
        root.mainloop()

    def __init__(self):
        
        items = mido.get_input_names()

        if len(items)==1:
            self.input_name = items[0]
        else:
            self.select_midi(items)

        self.UI = SmartKeyTrainerUI(self.start_exercise)
        self.audio_maker = AudioHandler()
        self.outport = mido.open_output()
        self.playing = set()
        self.target_chord_name, self.target_chord_list= "",[]
        self.chord_type  = None
        self.exercise = None
        self.target_notes = set(range(100))
        self.current_thread_id =0

    def octaviate_target_notes(self):
        for i in range(21,109):
            if i%12 in self.target_chord_list[0]:
                self.target_notes.add(i)

    def start_exercise(self,selected_chords,selected_progression,selected_scales,selected_sequence,mod,interval):
        """Start an exercise with the paramters selected by the user."""
        if mod is None:
            mod = True
        if selected_chords == None:
            selected_chords = [{60,64,67}]
        if selected_sequence == None:
            selected_sequence = 0
        if interval == None:
            interval = [21,108]

        self.UI.clear_keyboard()

        self.exercise = TargetGenerator(shift = selected_sequence,
                                        keep_scale=False,
                                        chord_shapes= selected_chords,
                                        scale_type = selected_scales,
                                        mod = mod,
                                        interval = interval)
        self.target_notes =self.exercise.get_targets()

        t1 = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
        t1.start()        

    def msg_handler(self, msg: mido.Message):

        if msg.type =="note on" and msg.note in self.playing:
            msg.type.__setattr__(type = "note_off")

        print(  f"""note recieved! 
                    value : {msg.note} 
                    message type : {msg.type}
                    msg in self.playing : {msg.note in self.playing}\n""")
        print("self.playing 1 : "+str(self.playing))
        print("targe notes : ", self.target_notes)

        if self.exercise != None:

            if msg.type == 'note_off' or (msg.type =="note_on" and msg.note in self.playing):
                if msg.note%12 in self.target_notes or msg.note in self.target_notes:
                    color = "vert"
                else:
                    color = "rouge"
                print("note off msg",msg.note,color)
                self.UI.unplay(msg.note,color)
                self.playing.remove(msg.note)

            elif msg.type == 'note_on':
                self.playing.add(msg.note)
                if msg.note%12 in self.target_notes or msg.note in self.target_notes:
                    color = "vert"
                else:
                    color = "rouge"
                        
                print("note on msg",msg.note,color)
                self.UI.play(msg.note,color)


            if  isinstance(self.exercise,TargetGenerator) :
                if self.exercise.target_reached(self.playing):
                    self.target_notes =self.exercise.get_targets()
                    chord_name =self.exercise.get_chord_name() 
                    self.UI.clear_keyboard()
                    self.color_blue_delay()
                    if chord_name !='':
                        self.UI.display_chord(chord_name)
            
    
            print("self.playing 10 +:"+str(self.playing))

    def color_blue_delay(self):
        self.current_thread_id+=1
        t1 = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
        t1.start()
                  
    def color_target_notes_blue(self,thread_id)->None:
        time.sleep(3)
        if self.current_thread_id == thread_id: 
            print("color bleu" ,self.target_notes)
            self.UI.play_list([(n,"bleu") for n in self.target_notes])
        
    def run(self):
        with mido.open_input(self.input_name, callback=self.msg_handler) as inport:
            self.UI.mainloop()


if __name__ == "__main__":
    trainer = SmartKeyTrainer()
    trainer.run()
    