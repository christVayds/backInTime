import pygame

class Music:

    def __init__(self):
        self.switch = False
        self.listMusics = [
            'audio/bg1.mp3',
            'audio/bg2.mp3'
        ]
        
        self.toPlay = 1
        pygame.mixer.music.load(self.listMusics[self.toPlay])

    def Play(self, loop=-1):
        pygame.mixer.music.play(loop)

    def Stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def switch_music(self):
        if self.switch:
            self.Stop()
            pygame.mixer.music.load(self.listMusics[self.toPlay])
            self.Play()
            self.switch = False 