from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

class SmartKeyTrainerUI:
    def __init__(self,main_event_handler):
      
        self.root = Tk()

        self.UI_event_handler = main_event_handler
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.label_chord_display = ttk.Label(self.mainframe,text="",font=("Arial", 25) )
        self.label_chord_display.grid(column=1, row=1, sticky=W)

        self.canvas = Canvas(self.root)
        self.img_keyboard =ImageTk.PhotoImage(file="image\pianokey_keyboard.jpg")
        self.height_piano,self.width_piano=self.img_keyboard.height(),self.img_keyboard.width()
        self.canvas.config(width=self.width_piano, height=self.height_piano)
        self.canvas.create_image(0,0,image =self.img_keyboard,anchor =NW)
        self.canvas.delete(self.img_keyboard)
        self.canvas.grid(row=3,column = 0,columnspan= 3)
        self.playing = dict()

        
        self.button = ttk.Button(self.root, text="basic seventh", command= lambda: self.UI_event_handler("Seventh"))
        self.button.grid(column=1, row=0)
        self.button = ttk.Button(self.root, text="AB voicings", command= lambda: self.UI_event_handler("AB voicings"))
        self.button.grid(column=1, row=1)

        self.button = ttk.Button(self.root, text="Diatonic Sequence", command= lambda: self.UI_event_handler("Diatonic Sequence"))
        self.button.grid(column=1, row=2)

        self.debugging = ttk.Label(self.mainframe,text="").grid(column=1, row=1, sticky=W)





        #set up dictionnaries for things
        self.note_filenames = {0: "do",1: "noir",2: "re",3: "noir",4: "mi",5: "fa",6: "noir",7: "sol",8: "noir",9: "la",10: "noir",11: "si" }   
        self.note_offsets = {0: 0,2: 107,3: 0,4: 142,5: 178,6: 0,7: 214,8: 0,9: 0,10: 0,11: 35}





        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def note_image_name(self,note):
        path = "image\\"
        print(note%12)
        if note ==108:
            return path + "plate_"
        elif note ==21:
            return path+"do_"
        else:
            return path+self.note_filenames[note%12]+"_"

    def play_list(self,msg):
        for (note,couleur) in msg:
            self.play(note,couleur)
    def play(self,note,couleur):
        note_name = self.note_image_name(note)+couleur+".png"
        print(note_name)
        note_image =ImageTk.PhotoImage(file= note_name)

        image_id = self.canvas.create_image(self.coord_x_note_image(note), 0, image=note_image, anchor=NW)
        self.playing[(note,couleur)] = {'tag': image_id, 'image': note_image}
    def clear_keyboard(self):
        for key in self.playing.keys():
            (note,couleur)=key
            self.canvas.delete(self.playing[(note,couleur)]['tag'])
        self.playing.clear()
    def clear_blue_keyboard(self):
        for key in self.playing.keys():
            (note,couleur)=key
            if couleur == "bleu":
                self.canvas.delete(self.playing[(note,couleur)]['tag'])
                self.playing.pop(key)
    def unplay(self, note,couleur):
        print("A")
        print(self.playing)

        if (note,couleur) in self.playing:
            print("B")
            self.canvas.delete(self.playing[(note,couleur)]['tag'])  # Delete the canvas item using the stored tag
            print("C")
            del self.playing[(note,couleur)]  # Remove the note from the dictionary
            print("D")
    def print(self,text):
        self.debugging(text = text)
    def mainloop(self):
        self.root.mainloop()
    def display_chord(self,chord):
        self.label_chord_display.configure(text = chord)


    # def coord_x_note_image(self,note) ->int:
    #     if note == 21:
    #         return 0
    #     noir =[1,3,6,8,10]
    #     if note%12 in noir:
    #         nb_noir = noir.index(note%12)
    #         if nb_noir>1:
    #             offset = 23+(nb_noir)*5
    #         else:
    #             offset=0
            
    #         return 93+nb_noir*35+offset+(251)*(note//12-2)
    #     if note%12 == 9:
    #         return -251+251*(note//12)
    #     if note%12 == 0:
    #         return 71+251*((note-24)//12)
    #     elif note%12 ==5:
    #         return 178+251*((note-24)//12)
    #     elif note%12 ==7:
    #         return 214+251*((note-24)//12)
    #     elif note%12 == 11:
    #         return 35+251*(1+(note-24)//12)
    #     if note%12 == 4:
    #         return 142+251*((note-24)//12)
    #     if note%12 ==2:
    #         return 107+251*((note-24)//12)   
        
    #     return 251
    #        # return 25
    #       #  return 93        

    def coord_x_note_image(self,note) ->int:
        if note == 21:
            return 0
        noir =[1,3,6,8,10]
        if note%12 in noir:
            nb_noir = noir.index(note%12)
            if nb_noir>1:
                offset = 23+(nb_noir)*5
            else:
                offset=0
            
            return 93+nb_noir*35+offset+(251)*(note//12-2)
        if note%12 == 9:
            return -251+251*(note//12)
        if note%12 == 0:
            return -431+251*(note//12)
        elif note%12 ==5:
            return -324+251*(note//12)
        elif note%12 ==7:
            return -288+251*(note//12)
        elif note%12 == 11:
            return -216+251*(note//12)
        if note%12 == 4:
            return -360+251*(note//12)
        if note%12 ==2:
            return -395+251*(note//12)   

           # return 25
          #  return 93



