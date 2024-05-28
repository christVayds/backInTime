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
        pygame.mixer.music.load(self.listMusics[self.toPlay])
        pygame.mixer.music.set_volume(0.2)

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

    def Change_Volume(self, amount):
        if amount > 0 and amount <= 1:
            pygame.mixer.music.set_volume(amount)