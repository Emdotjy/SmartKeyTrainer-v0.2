import time
import rtmidi
import random
import mido
import chords
from SmartKeyTrainerUI import SmartKeyTrainerUI
from audio_handler import *
import threading

class SmartKeyTrainer:

    def __init__(self):

        self.UI = SmartKeyTrainerUI(self.UI_event_handler)
        self.audio_maker = AudioHandler()
        self.outport = mido.open_output()
        self.playing = set()
        self.target_chord_name, self.target_chord_list= "",[]
        self.chord_type  = None
        self.exercise = None
        self.target_notes = set(range(100))
        self.current_thread_id =0
  


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
        t1 = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
        t1.start()        


    def msg_handler(self, msg: mido.Message):
        print(msg.note)
        if self.exercise != None:

            if msg.type == 'note_on':

                self.playing.add(msg.note)
                if msg.note%12 in self.target_notes or msg.note in self.target_notes:
                    color = "vert"
                else:
                    color = "rouge"
                
                print(msg.note,color)
                self.UI.play(msg.note,color)

            elif msg.type == 'note_off':
                if msg.note%12 in self.target_notes or msg.note in self.target_notes:
                    color = "vert"
                else:
                    color = "rouge"

                self.UI.unplay(msg.note,color)
                self.playing.remove(msg.note)


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
                    self.current_thread_id+=1
                    t1 = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
                    t1.start()
                    
                    
        
            print(1)
            if self.exercise == "Seventh":
                print(2)
                playing_mod = {i % 12 for i in self.playing}
                print(playing_mod)
                print(self.target_chord_list)
                print(self.target_notes)
                    
                if playing_mod in self.target_chord_list:
                    print(3)
                    self.UI.clear_keyboard()
                    print(4)
                    self.target_chord_list.clear()        
                    self.target_chord_name, self.target_chord_list= chords.generate_seventh_chord()
                    print(5)
                    self.target_notes.clear()
                    self.target_notes.update(self.target_chord_list[0])
                    print(6)
                    self.octaviate_target_notes()
                    print(8)
                    print(self.target_chord_name,self.target_chord_list)
                    self.UI.display_chord("                          ")
                    self.UI.display_chord(self.target_chord_name)
                    self.current_thread_id+=1
                    t = threading.Thread(target=self.color_target_notes_blue, args=(self.current_thread_id,), name=f"Thread-{self.current_thread_id}")
                    t.start()


                  
    def color_target_notes_blue(self,thread_id)->None:
        print("avant sleep")
        time.sleep(3)
        print("après sleep")
        if self.current_thread_id == thread_id: 
            print("color bleu" ,self.target_notes)
            self.UI.play_list([(n,"bleu") for n in self.target_notes])
        


    def run(self):

        with mido.open_input('Arturia KeyLab Essential 49 0', callback=self.msg_handler) as inport:
            self.UI.mainloop()

if __name__ == "__main__":
    trainer = SmartKeyTrainer()
    trainer.run()
    