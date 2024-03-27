import pygame

class AudioHandler:
    def __init__(self, max_number_of_note = 88):
            self.max_number_of_note  = max_number_of_note 

    def play_note(self, note):
        # Convert MIDI note number to frequency
        frequency = 440 * (2 ** ((note - 69) / 12))
        
        # Initialize Pygame audio
        pygame.init()
        
        # Set the audio driver and initialize Pygame mixer
        pygame.mixer.init()
        
        # Create a Pygame sound object with the desired frequency and play it
        self.sound = pygame.mixer.Sound( "piano_440.wav")
        self.sound.play()

    def stop(self,note):

        self.sound.stop()

 