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

    def select_midi(self,items):
        

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





        self.UI = SmartKeyTrainerUI(self.UI_event_handler)
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


  


    def UI_event_handler(self,button_pressed):
        self.UI.clear_keyboard()
        if button_pressed == "Destroy":
            self.mixer.quit()
        if button_pressed == "Seventh":
            self.target_chord_name, self.target_chord_list= chords.generate_seventh_chord()
            self.UI.display_chord(self.target_chord_name)
            self.exercise = "Seventh"
            self.target_notes.clear()
            self.target_notes.update(self.target_chord_list[0])
            self.octaviate_target_notes()
        if button_pressed == "AB voicings":
            self.target_chord_name, self.target_chord_list  = chords.generate_AB_voicing()
            self.UI.display_chord(self.target_chord_name)
            self.target_notes = set.union(self.target_chord_list[0],self.target_chord_list[1] )
            self.exercise = "AB voicings"
        if button_pressed == "Diatonic Sequence":
            self.exercise = TargetGenerator(shift = 1,keep_scale=True,chord_shapes=[{60,64,67}],scale_type = "Major")
            self.target_notes =self.exercise.get_targets()
        t1 = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
        t1.start()        



    def msg_handler(self, msg: mido.Message):

        if msg.type =="note on" and msg.note in self.playing:
            msg.type.__setattr__(type = "note_off")
        print("note recieved\n","value : " +str(msg.note),"\n message type : " +msg.type,"\n msg in self.playing : "+str(msg.note in self.playing)  )
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
            
            if self.exercise == "AB voicings":
                print(2)
                print(self.playing)
                print(self.target_chord_list)
                print(self.target_notes)
                if self.playing in self.target_chord_list:
                    for note in self.target_notes:
                        self.UI.unplay(note,"bleu")
     

                    self.UI.clear_keyboard() 
                    self.target_chord_list.clear()  
                    self.target_chord_name,self.target_chord_list = chords.generate_AB_voicing()               
                    self.target_notes.clear()
                    self.target_notes.update(self.target_chord_list[0])     
                      
                    self.UI.display_chord("                          ")
                    self.UI.display_chord(self.target_chord_name)
                    t1 = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
                    t1.start()
                    
            print("self.playing : 5"+str(self.playing))
        
            if self.exercise == "Seventh":
                playing_mod = {i % 12 for i in self.playing}
                    
                if playing_mod in self.target_chord_list:
                    self.UI.clear_keyboard()
                    self.target_chord_list.clear()        
                    self.target_chord_name, self.target_chord_list= chords.generate_seventh_chord()
                    self.target_notes.clear()
                    self.target_notes.update(self.target_chord_list[0])
                    self.octaviate_target_notes()
                    self.UI.display_chord("                          ")
                    self.UI.display_chord(self.target_chord_name)
                    self.color_blue_delay()
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
    