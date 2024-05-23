import pygame

class Music:

    def __init__(self):
        self.switch = False

        ####################### LIST ALL MUSIC HERE ####################### AERON
        self.listMusics = [
            'audio/bg1.mp3',
            'audio/bg2.mp3'
        ]
        
        self.toPlay = 1
        pygame.mixer.music.load(self.listMusics[self.toPlay]) # NAKA AUTO LOAD NA SIYA :) NO NEED TO LOAD MUSIC BG OKAY?

    def Play(self, loop=-1): ######## -1 means ilolop ang music, else hindi
        pygame.mixer.music.play(loop)

    def Stop(self): # STOP AND UNLOAD THE MUSIC
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def switch_music(self): # FOR SWITCHING MUSIC BACKGROUND
        if self.switch:
            self.Stop()
            pygame.mixer.music.load(self.listMusics[self.toPlay])
            self.Play()
            self.switch = False 

class SoundEffects: # GAWIN MO SOUND EFFECTS DITO

    def __init__(self):
        self.swicth = False
        self.listMusics = []